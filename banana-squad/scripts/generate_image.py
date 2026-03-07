#!/usr/bin/env python3
"""
Banana Squad - Gemini 3 Pro Image Generator

Reusable CLI script for generating images via the Gemini 3 Pro Image API.
Called by the Generator Agent for each prompt variant.

Usage:
    python3 generate_image.py --prompt "A ..." --output outputs/v1.png
    python3 generate_image.py --prompt "A ..." --aspect-ratio 16:9 --resolution 2K --output outputs/v1.png
    python3 generate_image.py --prompt "A ..." --reference ref1.png --reference ref2.png --output outputs/v1.png
"""

import argparse
import json
import os
import sys
import time

VALID_ASPECT_RATIOS = ["1:1", "16:9", "9:16", "3:2", "2:3", "4:3", "3:4", "4:5", "5:4", "21:9"]
VALID_RESOLUTIONS = ["1K", "2K", "4K"]


MODELS = [
    "gemini-3-pro-image-preview",
    "gemini-2.0-flash-exp-image-generation",
]

MAX_REF_DIMENSION = 1920  # Resize reference images to prevent API timeouts


def load_api_key():
    """Load GEMINI_API_KEY from environment or .env file.

    Searches multiple locations so subagents can find the key regardless
    of their working directory.
    """
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Try loading from .env in multiple locations
    try:
        from dotenv import load_dotenv

        search_dirs = [
            os.path.dirname(os.path.abspath(__file__)),          # scripts/
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # plugin root
            os.getcwd(),                                          # current dir
            os.path.expanduser("~"),                              # home
        ]
        for d in search_dirs:
            env_path = os.path.join(d, ".env")
            if os.path.exists(env_path):
                load_dotenv(env_path)
                key = os.environ.get("GEMINI_API_KEY")
                if key:
                    return key
    except ImportError:
        pass

    return None


def generate_image(prompt, aspect_ratio, resolution, output_path, reference_paths=None):
    """Generate an image using Gemini 3 Pro Image API."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return {
            "success": False,
            "output_path": output_path,
            "prompt_used": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "error": "google-genai package not installed. Run: pip install google-genai"
        }

    api_key = load_api_key()
    if not api_key:
        return {
            "success": False,
            "output_path": output_path,
            "prompt_used": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "error": "GEMINI_API_KEY not found. Set it in environment or .env file."
        }

    try:
        from PIL import Image
    except ImportError:
        Image = None

    try:
        client = genai.Client(api_key=api_key)

        # Build contents list
        contents = []

        # Add reference images if provided (resize large ones to prevent timeouts)
        if reference_paths:
            if Image is None:
                return {
                    "success": False,
                    "output_path": output_path,
                    "prompt_used": prompt,
                    "aspect_ratio": aspect_ratio,
                    "resolution": resolution,
                    "error": "Pillow not installed. Run: pip install Pillow"
                }
            for ref_path in reference_paths:
                if os.path.exists(ref_path):
                    ref_image = Image.open(ref_path)
                    # Resize if too large to prevent API timeouts
                    if max(ref_image.size) > MAX_REF_DIMENSION:
                        ratio = MAX_REF_DIMENSION / max(ref_image.size)
                        new_size = (int(ref_image.width * ratio), int(ref_image.height * ratio))
                        ref_image = ref_image.resize(new_size, Image.LANCZOS)
                    contents.append(ref_image)
                else:
                    return {
                        "success": False,
                        "output_path": output_path,
                        "prompt_used": prompt,
                        "aspect_ratio": aspect_ratio,
                        "resolution": resolution,
                        "error": f"Reference image not found: {ref_path}"
                    }

        # Add the text prompt
        contents.append(prompt)

        # If no reference images, contents is just the prompt string
        if not reference_paths:
            contents = prompt

        # Try each model in order (fallback on failure)
        last_error = None
        model_used = None

        for model_name in MODELS:
            try:
                # Pro model supports image_config; flash models reject it
                is_pro = "pro" in model_name and "flash" not in model_name
                if is_pro:
                    config = types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE'],
                        image_config=types.ImageConfig(
                            aspect_ratio=aspect_ratio,
                            image_size=resolution
                        ),
                    )
                else:
                    config = types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE'],
                    )

                # Generate
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )

                # Extract image from response
                image_saved = False
                response_text = ""

                if response.parts is None:
                    raise RuntimeError(f"Model {model_name} returned no parts (empty response)")

                for part in response.parts:
                    if part.text is not None:
                        response_text += part.text
                    elif part.inline_data is not None:
                        image = part.as_image()
                        # Ensure output directory exists
                        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                        image.save(output_path)
                        image_saved = True

                if not image_saved:
                    raise RuntimeError(
                        f"Model {model_name} returned no image. "
                        f"API text: {response_text or '(none)'}"
                    )

                model_used = model_name
                return {
                    "success": True,
                    "output_path": output_path,
                    "prompt_used": prompt,
                    "aspect_ratio": aspect_ratio,
                    "resolution": resolution,
                    "error": None,
                    "model_used": model_used,
                    "api_response_text": response_text if response_text else None
                }

            except Exception as model_err:
                last_error = str(model_err)
                # Continue to next model
                continue

        # All models failed
        return {
            "success": False,
            "output_path": output_path,
            "prompt_used": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "error": f"All models failed. Last error: {last_error}"
        }

    except Exception as e:
        error_msg = str(e)
        # Check for common API errors
        if "429" in error_msg or "rate" in error_msg.lower():
            error_msg = f"Rate limited by API. {error_msg}"
        elif "safety" in error_msg.lower() or "blocked" in error_msg.lower():
            error_msg = f"Content blocked by safety filter. {error_msg}"
        elif "400" in error_msg:
            error_msg = f"Bad request (check prompt/parameters). {error_msg}"

        return {
            "success": False,
            "output_path": output_path,
            "prompt_used": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "error": error_msg
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini 3 Pro Image API"
    )
    parser.add_argument(
        "--prompt", required=True,
        help="Narrative image description prompt"
    )
    parser.add_argument(
        "--aspect-ratio", default="16:9",
        choices=VALID_ASPECT_RATIOS,
        help="Image aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--resolution", default="2K",
        choices=VALID_RESOLUTIONS,
        help="Image resolution - MUST be uppercase (default: 2K)"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output file path (e.g., outputs/concept-v1-faithful.png)"
    )
    parser.add_argument(
        "--reference", action="append", default=[],
        help="Path to reference image (repeatable for multiple refs)"
    )

    args = parser.parse_args()

    # Validate resolution is uppercase
    if args.resolution != args.resolution.upper():
        print(json.dumps({
            "success": False,
            "error": f"Resolution must be uppercase: use '{args.resolution.upper()}' not '{args.resolution}'"
        }))
        sys.exit(1)

    result = generate_image(
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        output_path=args.output,
        reference_paths=args.reference if args.reference else None
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
