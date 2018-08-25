import math
import subprocess
from PIL import Image
import sys

# a (messy) python port of https://github.com/dom111/image-to-ansi, converting it into a nice cmd program
# TODO: do the unicode thing

def _toAnsi(img, oWidth=40, is_unicode=False):
    destWidth = img.width
    destHeight = img.height
    # produce a scale if the image is too big
    if destWidth > oWidth:
        scale = destWidth / oWidth
        destWidth = oWidth
        destHeight = math.floor(destHeight/scale)

    # resize to new size (i don't care about resizing method, can be nearest neighbour for all i care (default afaik))
    img = img.resize((destWidth, destHeight))
    # where the converted string will be put in
    ansi_string = ''

    i = 0
    n = img.width*img.height
    print(img.width, img.height)
    while i < n:
        r,g,b = map(str, img.getpixel((i % img.width, i//img.width)))
        if is_unicode:
            #TODO: this is a bit more complicated..
            pass
        else:
            ansi_string += '\x1B[48;2;' + r + ';' + g + ';' + b + 'm  '
            i += 1
            # newline
            if i % destWidth == 0:
                ansi_string += '\x1B[0m\n'
    print("num pixels:", i)

    return ansi_string

def convert(filename):
    im = Image.open(filename)
    stringo = _toAnsi(im)
    return stringo

if __name__ == "__main__":
    print(convert(sys.argv[1]))
