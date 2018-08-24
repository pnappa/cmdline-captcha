# cmdline-captcha
A command line interface for preventing bots via ascii image recognition

## Usage:
Follow the prompts - you may need to make your terminal have more room! The ascii art is pretty darn big
`$ python3 main.py`

## Requirements
 - python3
 - splinter (pip3 install splinter)
 - beautifulsoup4 (pip3 install bs4)
 - chromedriver (probably apt install chromedriver)

## TODO
 - [ ] Find some site that doesn't require JS to search images. At the moment, the memory usage is quite high just because we're running a full chrome instance for this
 - [ ] Larger wordbank (also try to pick ones that aren't really too ambiguous)
 - [ ] Scale the ascii down (there's probably a library to do this). The image currently doesn't fit!
 - [ ] Improve the ascii art generated, might need some image processing to increase contrast, and remove the background
    - this may be bad having too much contrast! this means that bots could make the ascii into images, and reverse img search..
 - [ ] Write this into a command-line program
