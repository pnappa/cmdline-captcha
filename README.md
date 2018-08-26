# cmdline-captcha
A command line interface for preventing bots via ascii image recognition

## Usage:
Follow the prompts. You'll need to download some images that are nice and recognisable.
`$ python3 improved.py`

## Requirements
 - python3
 - PIL (pip3 install PIL)

## TODO
 - [x] Find some site that doesn't require JS to search images. At the moment, the memory usage is quite high just because we're running a full chrome instance for this
 - [x] Larger wordbank (also try to pick ones that aren't really too ambiguous)
 - [x] Scale the ascii down (there's probably a library to do this). The image currently doesn't fit!
    - we can now generate ascii art at any size. There is an argument to `_toAnsi` that determines how wide the image is (in img2ansi.py).
    - increasing it too much likely means that its more likely that a bot could guess what the image is
 - [x] Improve the ascii art generated, might need some image processing to increase contrast, and remove the background
    - this may be bad having too much contrast! this means that bots could make the ascii into images, and reverse img search..
 - [ ] Write this into client/server tool
 - [ ] Pluggable scramblers. I'm talking writing ^H and lots of seeking. Might require some conversion to ncurses, so we can write to the screen arbitrarily
    - pluggable, so that other people can  

## Example
![example run](examplerun.png)
