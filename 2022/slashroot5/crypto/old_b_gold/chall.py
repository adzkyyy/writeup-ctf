#!/usr/bin/env python3
from random import *

class LCG:
    def __init__(self, seed):
        self.mod = (1<<16) + 1
        self.mult = randint(2,self.mod-2)
        self.inc = randint(2,self.mod-2)
        self.state = seed

    def next(self):
        self.state = (self.state * self.mult + self.inc) % self.mod
        return self.state

flag_content = open("flag.txt").read().strip()
seed = randint(2, (1<<16)-2)
r = LCG(seed)

while True:
    print("Menu:")
    print("[1] Guess flag")
    print("[2] Encrypt message")
    print("[3] Exit")
    inp = input("Input: ")

    if inp == "1":
        guess = input("Your guess: ")
        if guess == flag_content:
            print("NOICE!!!")
            print(f"Here is your flag: Slashroot5{{{flag_content}}}")
            exit()
        else:
            print("Nope....")
    elif inp == "2":
        msg = input("Your message: ")
        plain = flag_content + "||" + msg
        res = [r.next() ^ ord(x) for x in plain]
        print(f"Here is your encrypted message: {res}")
    elif inp == "3":
        exit()
    else:
        print("Unknown input...")
    print()
