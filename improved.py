import random
import string
import sys
import subprocess
import shutil
import imghdr
import os
import json
import re

# my beautiful library
import img2ansi

# return a number of image filenames that we can asciify
def get_image_filenames(word, directory, quantity=3):
    prefix = os.path.join(directory, word)
    basenames = list(map(lambda x: x.name, os.scandir(prefix)))
    print(list(basenames))
    ret = []
    for bname in random.sample(basenames, quantity):
        ret.append(os.path.join(prefix, bname))
    return ret

# each folder represents an image type
def pick_subject(directory):
    obj_names = [x.name for x in os.scandir(directory)]
    return random.choice(obj_names)

# the version that uses my library
def colour_ascii(filename):
    s = img2ansi.convert(filename, is_unicode=False, is_256=True)
    os.remove(filename)
    return s

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def correct_word(attempt, correct):
    return levenshtein_distance(attempt, correct) < 2

if __name__ == "__main__":
    # try:
        directory = "./obj_pics"
        word = pick_subject(directory)
        filenames = get_image_filenames(word, directory)
        print(filenames)
        for f in filenames:
            print(colour_ascii(f))
            guess = input("What is this object?\n> ")
            if correct_word(guess, word):
                print("correct!")
                sys.exit(0)
            print('incorrect...loading new image (of same object)')
        print("bad robot! it was actually a:", word)
        sys.exit(-1)
    #except Exception as e:
    #    print(e)
    #    print(word)

