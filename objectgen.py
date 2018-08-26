from bs4 import BeautifulSoup
import requests

def get_list():
    js = requests.get("https://www.randomlists.com/data/things.json").json()
    return js["RandL"]["items"]

if __name__ == "__main__":
    print("\n".join( [ "house","ant","towel","bee","sandal","drawer","phone","perfume","ipod","wallet","sunglasses","penguin","television","remote","clamp","sandpaper","plate","computer","window","piano","bracelet","vulture","clothes","keys","squirrel","sodacan","stopsign","chocolate","nailclippers","needle","paper","speakers","sailboat","lamp","rhino","racoon","rug","watch","lamp","shoes","doll","cat","rat","box","button","paintbrush","pool","sponge","tireswing","rubberband","mousepad","flower","tissuebox","gorilla","giraffe","badger","carrot","tomato","monitor","knife","mirror","flag","whale","headphones","bag","car","bottle","horse","sock","newspaper","radio","shirt","tv","mop","toothpaste","eagle","thread","balloon","bookmark","dragon","helmet","beaver","candle","photoalbum","cow","bed","boombox","screw","door","soap","pencil","pillow","shovel","bread","stockings","vase","pictureframe","frog","pen","cup","couch","bowl","phone","kangaroo","fridge","crab","milk","CD","thermometer","banana","swan","washingmachine","monkey","goat","camera","zebra","camel","duck","fork","bird","chalk","clock","book","magnet","dog","rabbit","slipper","bottle","stingray","toothbrush","sharpie","spoon","chair","shark","ring","lace","turtle","hairbrush","deodorant","rubberduck","eraser","sidewalk","canvas","glasses","keyboard","bear","glass","hanger","alligator","desk","floor","sofa","fish","bottlecap","toothpick","butterfly","cookie","claypot","money","car","owl","toilet","elephant","apple","controller","fork","table","tweezer","lion","pants","zipper","brocolli","tree","purse","pig","truck"]))
   # 
   # 

   # s = set()
   # # removed: "platypus", 
   # s |= set(["zebra", "cow", "horse", "frog", "dog", "monkey", "owl", "shark", "badger", "fish", "turtle", "beaver", "alligator", "bear", "bird", "dragon", "rhino", "ant", "cat", "elephant", "butterfly", "camel", "duck", "crab", "eagle", "whale", "giraffe", "goat", "gorilla", "rabbit", "kangaroo", "penguin", "lion", "stingray", "rat", "pig", "racoon", "turkey", "swan", "vulture", "bee", "squirrel"])
   # for i in range(1):
   #     s |= set(get_list())
   # print("\n".join(list(s)))

