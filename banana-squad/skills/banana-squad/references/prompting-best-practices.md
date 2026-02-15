# Image Prompt Crafting Guide

> Best practices for writing prompts that produce high-quality images with Gemini 3 Pro Image API.

## The #1 Rule

**Describe the scene as a narrative paragraph. NEVER use keyword lists.**

A descriptive paragraph always produces better images than disconnected words. Think of it as writing a brief screenplay scene description.

BAD (keyword list):
```
sunset, beach, golden hour, waves, warm tones, wide angle, peaceful
```

GOOD (narrative paragraph):
```
A wide-angle photograph of a secluded tropical beach at golden hour, with warm amber sunlight casting long shadows across pristine white sand. Gentle turquoise waves lap at the shoreline, their crests catching the last rays of daylight. The sky transitions from deep orange near the horizon through coral pink to soft lavender overhead, with a few wispy clouds adding texture. Shot with a 24mm lens at f/8, emphasizing the vast, peaceful emptiness of the scene.
```

## Prompt Template

Every prompt should include these elements woven into a natural paragraph:

1. **Subject** - What is the main focus of the image?
2. **Environment/Setting** - Where is the scene? What surrounds the subject?
3. **Lighting** - What kind of light? Direction, color temperature, quality?
4. **Camera/Perspective** - What angle? What lens? What depth of field?
5. **Mood/Atmosphere** - What emotion should the viewer feel?
6. **Textures/Materials** - What surfaces, fabrics, materials are visible?
7. **Colors** - What palette dominates? Any specific brand colors?
8. **Composition** - How are elements arranged? Rule of thirds? Symmetry?

## Photography Terms for Realism

Use these to control the "camera" and achieve photorealistic results:

### Lens & Camera
- `85mm portrait lens` - flattering compression for faces
- `24mm wide-angle` - expansive landscapes, interiors
- `macro lens` - extreme close-ups of small details
- `tilt-shift` - miniature effect
- `f/1.8 shallow depth of field` - blurred background (bokeh)
- `f/16 deep focus` - everything sharp

### Lighting
- `golden hour` - warm, soft, low-angle sunlight
- `blue hour` - cool twilight tones
- `Rembrandt lighting` - dramatic portrait lighting with triangle on cheek
- `softbox lighting` - even, flattering studio light
- `rim lighting` - edge light creating halo/outline
- `natural window light` - soft directional daylight
- `high-key` - bright, minimal shadows
- `low-key` - dark, dramatic shadows

### Angles
- `eye-level shot` - neutral, relatable
- `low-angle perspective` - makes subject appear powerful
- `bird's eye view` - overhead looking down
- `Dutch angle` - tilted for tension/unease
- `over-the-shoulder` - creates depth, context

## Semantic Negatives

Describe what you WANT, not what you don't want.

BAD: `no text, no watermark, no blur`
GOOD: `clean composition with sharp focus throughout, unobstructed view`

BAD: `no people, no cars`
GOOD: `a deserted empty street in the early morning hours`

## Style-Specific Tips

### Photorealistic
```
A photorealistic [shot type] of [subject], [action/expression], set in [environment].
Illuminated by [lighting], creating a [mood] atmosphere.
Captured with [camera/lens], emphasizing [textures/details].
```

### Infographic / Diagram
```
A clean, professional infographic about [topic] with a [color scheme] palette.
The layout uses [structure: grid/flow/radial] to present [data type].
Key statistics are displayed in [bold/large] typography with [chart types].
White space is used intentionally to create clear visual hierarchy.
```

### Product Photography
```
A high-resolution, studio-lit product photograph of [product] on [surface].
Lighting: [setup] to [purpose]. Camera: [angle] to showcase [feature].
Ultra-realistic, sharp focus on [detail].
```

### Icon / Sticker
```
A [style] sticker of [subject], featuring [characteristics] and a [color palette].
Bold, clean outlines, [shading style]. Background: [color/transparent].
```

### Text in Image
```
Create a [image type] for [brand/concept] with the text "[exact text]"
in a [font style]. Design: [style description], color scheme: [colors].
```

## Aspect Ratio Selection Guide

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Social media post | 1:1 | Instagram, Twitter feed |
| YouTube thumbnail | 16:9 | Standard video format |
| Instagram Story/Reel | 9:16 | Vertical mobile format |
| Infographic | 9:16 or 2:3 | Tall vertical for scrolling |
| Website hero | 21:9 | Ultra-wide banner |
| Product photo | 4:5 or 1:1 | E-commerce standard |
| Presentation slide | 16:9 | Standard slide format |
| Print poster | 3:2 or 4:3 | Common print ratios |

## Common Mistakes

1. **Too vague**: "a nice picture of a dog" -> Add breed, setting, lighting, mood
2. **Keyword stuffing**: "4K HDR ultra realistic masterpiece" -> These don't help
3. **Conflicting instructions**: "minimalist but with lots of detail" -> Pick one direction
4. **Ignoring composition**: Not specifying how elements relate spatially
5. **Missing context**: "create a logo" vs "logo for a high-end minimalist skincare brand targeting women 25-40"
