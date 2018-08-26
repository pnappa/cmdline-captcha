import requests
import random
import bs4
from bs4 import BeautifulSoup
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

num_guesses = 5
word_bank = ["horse", "cow", "car", "windmill", "cup"]
image_size = 200
# the sizes of images that we can retrieve from flickr 
# they all have different sizes, but lets pick the large one (l)
# flickr_sizes = ['q', 'n', 'c', 'sq', 'm', 's', 'l', 'z', 't'] 
# ordered preference of sizes (largest to smallest atm)
flicker_size_prefs = ["l", "c", "z", "m", "n", "q", "sq", "t"]

# search flickr and get a series of URLs
def get_image_urls(word):
    query_str = "https://www.flickr.com/search/?sort=relevance&text={}&fr=sfp&fr2=piv-web&ytcheck=1".format(word)
    r = requests.get(query_str)
    search_reg = re.search("modelExport:.*", r.text)
    # extract the js that has all this stuff
    modelExp = r.text[search_reg.start():search_reg.end()]
    # convert to well formed json, so we can query it
    modelExp = "{" + modelExp.replace("modelExport", '"modelExport"')[:-1] + "}"
    j = json.loads(modelExp)
    j = j["modelExport"]["main"]['search-photos-lite-models'][0]["photos"]["_data"]
    random_chunks = random.sample(j, num_guesses)
    ret_urls = []
    for chunk in random_chunks:
        for sz in flicker_size_prefs:
            if sz in chunk["sizes"]:
                url = "https:" + chunk["sizes"][sz]["url"]
                # strip out weird get query at the end (having it there causes a 506 error or something...)
                url = url.replace("?zz=1", "")
                ret_urls.append(url)
                break
    return ret_urls

def get_ascii(url):
    # XXX: we use a shell command because I can't get the python requests thing working...
    html_result = os.popen("""curl 'http://www.glassgiant.com/ascii/ascii.php' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://www.glassgiant.com' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryZh7v5BlhNSRPM1Il' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://www.glassgiant.com/ascii/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' --data-binary $'------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="maxwidth"\r\n\r\n{0}\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="fontsize"\r\n\r\n8\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="webaddress"\r\n\r\n{1}\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="ggfile"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\r\n\r\n3145728\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="negative"\r\n\r\nN\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il--\r\n' --compressed 2>/dev/null""".format(image_size,url)).read()

    b = BeautifulSoup(html_result, "html.parser")
    # extract the ascii art from the html
    ascii_art = b.table.tr.td.font.children
    # then, clean up so we get a nice string
    res = []
    for a in ascii_art:
        if type(a) == bs4.element.NavigableString:
            res.append(str(a))
    return "".join(res)

def pick_subject():
    return random.choice(word_bank)

def download_img(url):
    # come up with a random file name 10 letters long
    directory = "{}.png".format("".join([random.choice(string.ascii_letters) for _ in range(10)]))
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

# the version that uses my library
def colour_ascii(url):
    filename = download_img(url)
    s = img2ansi.convert(filename, is_unicode=False, is_256=True)
    os.remove(filename)
    return s

if __name__ == "__main__":
    word = random.choice(word_bank)
    urls = get_image_urls(word)
    for url in urls:
        #print(get_ascii(url))
        print(colour_ascii(url))
        guess = input("What is this object?\n> ")
        if guess == word:
            print("correct!")
            sys.exit(0)
        print('incorrect...loading new image (of same object)')
    print("bad robot! it was actually a:", word)
    sys.exit(-1)

