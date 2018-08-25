import requests
import random
import bs4
from bs4 import BeautifulSoup
import sys
import subprocess
import shutil
import imghdr
import os
import json
import re

num_guesses = 5
word_bank = ["horse", "cow", "car", "windmill", "cup"]
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
        print(chunk["sizes"].keys())
        for sz in flicker_size_prefs:
            if sz in chunk["sizes"]:
                ret_urls.append("https:" + chunk["sizes"][sz]["url"])
                break
    return ret_urls

def get_ascii(url):
    url = url.replace("?zz=1", "")
    # XXX: we use a shell command because I can't get the python requests thing working...
    html_result = os.popen("""curl 'http://www.glassgiant.com/ascii/ascii.php' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://www.glassgiant.com' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryZh7v5BlhNSRPM1Il' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://www.glassgiant.com/ascii/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' --data-binary $'------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="maxwidth"\r\n\r\n160\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="fontsize"\r\n\r\n8\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="webaddress"\r\n\r\n{}\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="ggfile"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\r\n\r\n3145728\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\r\nContent-Disposition: form-data; name="negative"\r\n\r\nN\r\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il--\r\n' --compressed""".format(url)).read()

    b = BeautifulSoup(html_result, "html.parser")
    # extract the ascii art from the html
    ascii_art = b.table.tr.td.font.children
    # then, clean up so we get a nice string
    res = []
    for a in ascii_art:
        if type(a) == bs4.element.NavigableString:
            res.append(str(a))
    return "".join(res)

#    
#    # use session, because this uses PHPSESSIDs to yield data...
#    session = requests.session()
#    # do this to get a cookie
#    session.get("http://www.glassgiant.com/ascii/")
#    print(session.cookies)
#    # possibly the best site to exist: https://curl.trillworks.com/
#    # used this to convert from cURL (right click, copy as cURL from chrome dev tools) to python requests!
#    headers = {
#        'Connection': 'keep-alive',
#        'Pragma': 'no-cache',
#        'Cache-Control': 'no-cache',
#        'Origin': 'http://www.glassgiant.com',
#        'Upgrade-Insecure-Requests': '1',
#        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryZh7v5BlhNSRPM1Il',
#        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#        'Referer': 'http://www.glassgiant.com/ascii/',
#        'Accept-Encoding': 'gzip, deflate',
#        'Accept-Language': 'en-US,en;q=0.9',
#    }
#
#    data = '$------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="maxwidth"\\r\\n\\r\\n80\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="fontsize"\\r\\n\\r\\n8\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="webaddress"\\r\\n\\r\\n{}\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="ggfile"; filename=""\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\\r\\n\\r\\n3145728\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il\\r\\nContent-Disposition: form-data; name="negative"\\r\\n\\r\\nN\\r\\n------WebKitFormBoundaryZh7v5BlhNSRPM1Il--\\r\\n'.format(url)
#
#    response = session.post('http://www.glassgiant.com/ascii/ascii.php', headers=headers, data=data) 
#    print(response.text)
#
#    # TODO: replace with requests
#    # submit everything... now we're able to not even need to download the image!
#    browser.visit("http://www.glassgiant.com/ascii/")
#    browser.select("maxwidth", "120")
#    browser.fill("webaddress", url)
#    browser.find_by_css('input[type="submit"]')[0].click()
    # TODO: parse from the resulting page

if __name__ == "__main__":
    urls = get_image_urls("horse")
    print(urls)
    print(get_ascii(urls[0]))
    input()
