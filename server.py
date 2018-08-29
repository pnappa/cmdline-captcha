import time
import socket
import improved
import os
import struct
import subprocess

# creating a socket object
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

# get local Host machine name
host = ''
port = 6963
obj_dir = './example_objects'

# bind to pot
s.bind((host, port))

# Que up to 5 requests
s.listen(5)

while True:
    # establish connection
    clientSocket, addr = s.accept()
    print("got a connection from %s" % str(addr))
    #print(os.popen('lsof -i:{} | cut -f 3 -d" " | grep -v "^$"'.format(addr[1])).read())
    word = improved.pick_subject(obj_dir)
    print("getting them to guess a", word)
    filenames = improved.get_image_filenames(word, obj_dir)
    for f in filenames:
        ascii_art = improved.colour_ascii(f)
        clientSocket.send(ascii_art.encode("utf-8"))
        clientSocket.send(b"What is this object?\n")
        guess = clientSocket.recv(1024).decode('utf-8').strip()
        print("their guess:", guess)
        if improved.correct_word(guess, word):
            clientSocket.send(b"Wow, well done!\n")
            break
        else:
            clientSocket.send(b"unlucky...\n")

    clientSocket.close()

