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


def load_api_key():
    """Load GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Try loading from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
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
        client = genai.Client(api_key=api_key)

        # Build contents list
        contents = []

        # Add reference images if provided
        if reference_paths:
            from PIL import Image
            for ref_path in reference_paths:
                if os.path.exists(ref_path):
                    ref_image = Image.open(ref_path)
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

        # Build config
        config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            ),
        )

        # Generate
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=config
        )

        # Extract image from response
        image_saved = False
        response_text = ""

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
            return {
                "success": False,
                "output_path": output_path,
                "prompt_used": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "error": "No image returned by API. Possible safety filter or prompt issue.",
                "api_response_text": response_text
            }

        return {
            "success": True,
            "output_path": output_path,
            "prompt_used": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "error": None,
            "api_response_text": response_text if response_text else None
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
