# reeded-glass 🥂

An interactive WebGL poster that mimics frosted reeded glass using shaders. I've created this shader at the request of my friend. It's supposed to mimic a very trendy effect [like the one here](https://www.youworkforthem.com/graphic/E6379/reeded-glass-displacement-system).

## Showcase

![Reeded Glass Effect](./reed-glass.gif)

## Features

* **Two-Pass Rendering:** To achieve this effect, the scene is rendered in two passes. The first pass renders the entire viewport into a texture, while the second projects it onto the glass with applied refraction and displacement.
* **Smooth drift:** The camera continuously drifts along the lemniscate (infinity) loop. This ambient movement is blended with mouse and touch for smooth response.
* **Grain, tint, etc.:** I've dropped in some grain, blur and tint to achieve more cinematic look.

## Quick Start

To run the development server locally:

```bash
bun run dev
```
