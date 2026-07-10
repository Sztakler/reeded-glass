import argparse
import struct

import cairosvg
import numpy as np

from PIL import Image
from scipy.ndimage import distance_transform_edt

import matplotlib.pyplot as plt


def svg_to_alpha(svg_path, size):

    png = cairosvg.svg2png(
        url=svg_path,
        output_width=size,
        output_height=size
    )

    with open("_temp.png", "wb") as f:
        f.write(png)

    img = Image.open("_temp.png").convert("RGBA")

    alpha = np.array(img)[:, :, 3]

    return alpha / 255.0



def generate_sdf_3d(alpha, z_resolution, depth):

    inside = alpha > 0.5


    print("Generating 2D distance...")


    outside = distance_transform_edt(
        ~inside
    )

    inside_dist = distance_transform_edt(
        inside
    )


    sdf2d = outside - inside_dist



    print("Extruding into 3D...")


    h,w = alpha.shape


    sdf3d = np.zeros(
        (
            z_resolution,
            h,
            w
        ),
        dtype=np.float32
    )


    half = z_resolution / 2


    for z in range(z_resolution):

        zpos = abs(
            (z-half)/half
        )

        zdist = (
            zpos * depth * h
        )


        sdf_slice = sdf2d.copy()


        sdf_slice = np.maximum(
            sdf_slice,
            zdist
        )


        sdf3d[z] = sdf_slice




    m = np.max(
        np.abs(sdf3d)
    )

    sdf3d /= m


    return sdf3d



def save_sdf(path, sdf):

    with open(path,"wb") as f:

        z,y,x = sdf.shape


        f.write(
            struct.pack(
                "III",
                x,
                y,
                z
            )
        )


        f.write(
            sdf.tobytes()
        )



def main():

    parser = argparse.ArgumentParser()


    parser.add_argument(
        "svg"
    )


    parser.add_argument(
        "output"
    )


    parser.add_argument(
        "--size",
        type=int,
        default=256
    )


    parser.add_argument(
        "--z",
        type=int,
        default=32
    )


    parser.add_argument(
        "--depth",
        type=float,
        default=0.25,
        help="relative extrusion depth"
    )


    args = parser.parse_args()



    print("Rendering SVG...")


    alpha = svg_to_alpha(
        args.svg,
        args.size
    )


    print(
        "Generating 3D SDF..."
    )


    sdf = generate_sdf_3d(
        alpha,
        args.z,
        args.depth
    )


    print(
        "Saving..."
    )


    save_sdf(
        args.output,
        sdf
    )


    print(
        "Done:",
        sdf.shape
    )




    plt.imshow(
        sdf[sdf.shape[0]//2],
        cmap="coolwarm"
    )

    plt.colorbar()

    plt.show()



if __name__=="__main__":
    main()
