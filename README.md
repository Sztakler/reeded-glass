# reeded-glass 🥂

An interactive WebGL poster that mimics frosted reeded glass using shaders. I've created this shader at the request of my friend. It's supposed to mimic a very trendy effect [like the one here](https://www.youworkforthem.com/graphic/E6379/reeded-glass-displacement-system).

## Showcase

**[>> Try it yourself <<](https://sztakler.github.io/reeded-glass/)**

![Reeded Glass Effect](./images/reed-glass.gif)

## Features

* **Two-Pass Rendering:** To achieve this effect, the scene is rendered in two passes. The first pass renders the entire viewport into a texture, while the second projects it onto the glass with applied refraction and displacement.
* **Smooth drift:** The camera continuously drifts along the lemniscate loop. This ambient movement is blended with mouse and touch for smooth response.
* **Grain, tint, etc.:** I've dropped in some grain, blur and tint to achieve more cinematic look.
* **Config Persistence:** You can save your custom setups as JSON files and load them back into the scene.

## Quick Start

To run the development server locally:

```bash
bun install
bun run dev
```

## How to use

1. Upload your own `Bottom` (background) and `Top` (foreground) images.
2. Use the GUI panel to tweak the refraction, blur, and shatter intensity.
3. Once satisfied, hit `Save Config` to export your unique look as a `.json` file.
4. Use `Load Config` to restore your previously saved compositions.

## Roadmap

- [ ] **Pattern Variety**: Implement new geometric patterns (circles, spirals, radial symmetry).
- [ ] **Performance Optimization**: Replace multi-sampling blur with a more efficient convolution approach or optimized mipmap-based blurring.
- [ ] **Input Validation**: Add checks for uploaded file formats and size limits (max 5MB) before processing images.
- [ ] **UI/UX Improvements**: Add a mobile-friendly touch toggle and better feedback during image loading.
- [ ] **Advanced Refraction**: Explore dynamic refraction mapping based on custom displacement maps.
