from splinter import Browser
import random
from bs4 import BeautifulSoup
import sys
import shutil
import imghdr
import requests
import os

num_guesses = 5
word_bank = ["horse", "cow", "car", "windmill", "cup"]
query_str = "https://duckduckgo.com/?q={}&t=hj&ia=images&iax=images"
ascii_site = "https://picascii.com/"

browser = Browser("chrome")

def pick_subject():
    return random.choice(word_bank)

def el2url(element):
    img_data = element.outer_html
    b = BeautifulSoup(img_data, "html.parser")
    for i in b.children:
        return "https:" + i["data-src"]

def download_img(url):
    directory = "img.png"
    response = requests.get(url, stream=True)
    with open(directory, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    filename = os.path.join(os.getcwd(), directory)
    correctftype = imghdr.what(filename)
    filename2 = filename.replace("png", correctftype)
    shutil.move(filename, filename2)
    # return the downloaded file name
    return filename2

def get_image_urls(word): 
    # Visit URL
    url = query_str.format(word)
    browser.visit(url)
    piccys = browser.find_by_css('img[class="tile--img__img  js-lazyload"]')
    img_urls = list(map(el2url, random.sample(piccys, num_guesses)))
    return img_urls


def get_ascii(filename):
    browser.visit(ascii_site)
    browser.attach_file("imageupload", filename)
    browser.find_by_css('input[type="submit"]')[0].click()
    ascii_art = browser.find_by_css('pre[class="white"]')[0].text

    return ascii_art

if __name__ == "__main__":
    word = pick_subject()
    url_images = get_image_urls(word)
    for url in url_images:
        filename = download_img(url)
        ascii_art = get_ascii(filename)

        print(ascii_art)
        guess = input("hello human. what is this object? (you'll receive a different image if you get this wrong\n")
        if guess == word:
            print('well done!')
            sys.exit(0)
        print("not quite... downloading another image of same subject")

    print('go away robot!!')
    sys.exit(-1)

