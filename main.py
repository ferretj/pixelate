import sys
import numpy as np
import argparse
from PIL import Image, ImageEnhance

def pixellize(**kwargs):

    # load image
    #img_name = "test.jpg"
    #img_name = "./examples/original/test.jpg"
    if "img_path" not in list(kwargs.keys()):
        raise KeyError("Image path is not given.")
    elif "save_path" not in list(kwargs.keys()):
        raise KeyError("Save path is not given.")
    else:
        img_name = kwargs["img_path"]
        save = kwargs["save_path"]

    img = Image.open(img_name)
    img_size = img.size

    # boost saturation of image 
    sat_booster = ImageEnhance.Color(img)
    img = sat_booster.enhance(float(kwargs.get("saturation", 1.25)))

    # increase contrast of image
    contr_booster = ImageEnhance.Contrast(img)
    img = contr_booster.enhance(float(kwargs.get("contrast", 1.2)))

    # reduce the number of colors used in picture
    img = img.convert('P', palette=Image.ADAPTIVE, colors=int(kwargs.get("n_colors", 10)))

    # reduce image size
    superpixel_size = int(kwargs.get("superpixel_size", 10))
    reduced_size = (img_size[0] // superpixel_size, img_size[1] // superpixel_size)
    img = img.resize(reduced_size, Image.BICUBIC)

    # resize to original shape to give pixelated look
    img = img.resize(img_size, Image.BICUBIC)

    # plot result
    img.save(save)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('img_path')
    parser.add_argument('save_path')
    parser.add_argument('n_colors', default=10 , nargs="?")
    parser.add_argument('superpixel_size', default=10, nargs="?")
    parser.add_argument('saturation', default=1.25 , nargs="?")
    parser.add_argument('contrast', default=1.2 , nargs="?")
    kwargs = vars(parser.parse_args())

    print type(kwargs)

    pixellize(**kwargs)