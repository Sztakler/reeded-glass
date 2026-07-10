import argparse
import struct
import cairosvg
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import distance_transform_edt

def svg_to_alpha(svg_path, size):
    png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
    with open("_temp.png", "wb") as f:
        f.write(png_data)
    img = Image.open("_temp.png").convert("RGBA")
    return np.array(img)[:, :, 3] / 255.0

def generate_2d_sdf(alpha):
    inside = alpha > 0.5
    out_dist = distance_transform_edt(~inside)
    in_dist = distance_transform_edt(inside)
    return (out_dist - in_dist).astype(np.float32)

def generate_sdf_3d(alpha, z_res, depth, disp=0.05):
    sdf2d = generate_2d_sdf(alpha)
    h, w = alpha.shape
    noise = np.random.randn(z_res, h, w).astype(np.float32) * disp
    sdf3d = np.zeros((z_res, h, w), dtype=np.float32)
    half_z = z_res / 2.0
    extrusion = z_res * depth

    for z in range(z_res):
        z_pos = (abs(z - half_z) - extrusion) + noise[z]
        sdf3d[z] = np.maximum(sdf2d, z_pos * (w / z_res))

    sdf3d /= np.max(np.abs(sdf3d))
    return sdf3d.astype(np.float32)

def save_sdf(path, sdf):
    z, y, x = sdf.shape
    with open(path, "wb") as f:
        f.write(struct.pack("III", x, y, z))
        f.write(sdf.tobytes())

def preview_sdf(sdf):
    mid_z, mid_y, mid_x = [s // 2 for s in sdf.shape]
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(sdf[mid_z, :, :], cmap="coolwarm", origin='lower')
    plt.title("XY")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(sdf[:, mid_y, :], cmap="coolwarm", origin='lower', aspect='auto')
    plt.title("XZ")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(sdf[:, :, mid_x], cmap="coolwarm", origin='lower', aspect='auto')
    plt.title("YZ")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="SVG to 3D SDF")
    parser.add_argument("svg", help="Input SVG")
    parser.add_argument("output", help="Output file")
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--z", type=int, default=32)
    parser.add_argument("--depth", type=float, default=0.25)
    args = parser.parse_args()

    alpha = svg_to_alpha(args.svg, args.size)
    sdf = generate_sdf_3d(alpha, args.z, args.depth)
    save_sdf(args.output, sdf)
    print(f"Done! Shape: {sdf.shape}")
    preview_sdf(sdf)

if __name__ == "__main__":
    main()
