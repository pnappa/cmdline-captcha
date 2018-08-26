import math
import subprocess
from PIL import Image
import sys
import functools


# a (messy) python port of https://github.com/dom111/image-to-ansi, converting it into a nice cmd program
# TODO: do the unicode thing

# convert a colour to one that can be displayed in a shitty terminal (sorry guys)
def _rgb_to_256(r,g,b):
    r,g,b = map(int, (r,g,b))
    # i actually don't know how he came up with these colours
    colours = []
    colours.append([0, 0, 0, 0])
    colours.append([128, 0, 0, 1])
    colours.append([0, 128, 0, 2])
    colours.append([128, 128, 0, 3])
    colours.append([0, 0, 128, 4])
    colours.append([128, 0, 128, 5])
    colours.append([0, 128, 128, 6])
    colours.append([192, 192, 192, 7])
    colours.append([128, 128, 128, 8])
    colours.append([255, 0, 0, 9])
    colours.append([0, 255, 0, 10])
    colours.append([255, 255, 0, 11])
    colours.append([0, 0, 255, 12])
    colours.append([255, 0, 255, 13])
    colours.append([0, 255, 255, 14])
    colours.append([255, 255, 255, 15])

    for r1 in [0, 95, 135, 175, 215, 255]:
        for g1 in [0, 95, 135, 175, 215, 255]:
            for b1 in [0, 95, 135, 175, 215, 255]:
                colours.append([r1,g1,b1, 16 + int(str(math.floor(5 * r1/255)) + 
                                            str(math.floor(5 * g1/255)) + 
                                            str(math.floor(5 * b1/255)),6)])

    for s in [8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238]:
        colours.append([s,s,s, 232 + math.floor(s/10)])

    # get the best term colour
    def best(candidates, source):
        # based on the distance from the populated colour table - closest wins!
        return min(candidates, key=lambda x: abs(x[0] - source[0]) + abs(x[1] - source[1]) + abs(x[2] - source[2]))

    return best(colours, [r,g,b])[3]

def _pix_to_escape(r,g,b,is_256, is_unicode):
    pass 

def _toAnsi(img, oWidth=40, is_unicode=False, is_256=False):
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
    while i < n:
        r,g,b = map(str, img.getpixel((i % img.width, i//img.width)))
        if is_256:
            if is_unicode:
                raise NotImplementedError("unicode functionality not implemented yet.. idk what they did")
                #bg_col = _rgb_to_256(r,g,b)
                ## is the next row's colour
                #rprime, gprime, bprime = map(str, img.getpixel((i%img.width, i//img.width + 1)))
                #fg_col = _rgb_to_256(rprime, gprime, bprime)
                #pass
            else:
                ansi_string += '\x1B[48;5;' + str(_rgb_to_256(r,g,b)) + 'm  '
                i += 1
                if i % destWidth == 0:
                    ansi_string += '\x1B[0m\n'
        else:
            if is_unicode:
                #TODO: this is a bit more complicated..
                raise NotImplementedError("unicode functionality not implemented yet.. idk what they did")
            else:
                ansi_string += '\x1B[48;2;' + r + ';' + g + ';' + b + 'm  '
                i += 1
                # newline
                if i % destWidth == 0:
                    ansi_string += '\x1B[0m\n'

    return ansi_string

def convert(filename, is_unicode=False, is_256=False):
    # open the img, but convert to rgb because this fails if grayscale (assumes pixels are at least triplets)
    im = Image.open(filename).convert('RGB')
    stringo = _toAnsi(im, is_unicode=is_unicode, is_256=is_256)
    return stringo

if __name__ == "__main__":
    print(convert(sys.argv[1], is_256=True))
