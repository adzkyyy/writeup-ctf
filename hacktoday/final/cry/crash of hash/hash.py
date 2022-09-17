#!/usr/bin/python3
from hashlib import md5
from string import ascii_uppercase as ALLCHAR
from random import seed, choices
from time import time
from math import floor


seed(floor(time()))
SECRET = "".join(choices(ALLCHAR, k=4)).encode()
FLAG = open("flag.txt", "r").read()


def show_menu():
    print(
        """
Select menu:
[1] Play.
[2] Get secret.
[3] Exit"""
    )


def get_digest(msg):
    return md5(msg).hexdigest()


def get_secret():
    return get_digest(SECRET)


def ask_string(n):
    print(f"Please enter string {n}")
    string = input("> ")
    string = bytes.fromhex(string)
    if string[:4] == SECRET:
        return string
    return False


def get_flag():
    print("\n# Enter two different strings.")
    s1 = ask_string("string 1")
    s2 = ask_string("string 2")
    if not s1 or not s2:
        return "Wrong secret."
    if s1 == s2:
        return "Crash!"
    if get_digest(s1) != get_digest(s2):
        return "Something went wrong (?)"
    return FLAG


def main():
    print("Welcome to Crash of Hash!")
    print("Crash of Hash is a fun game that can makes you smash your brain.")
    print(
        "The game is simple, to get the flag, you have to give us two different strings (in hex) with the same md5 hash."
    )
    print("Psst... To be honest, it's not that simple.")
    while True:
        show_menu()
        op = input("> ")
        if op == "1":
            print(f"# {get_flag()}")
        elif op == "2":
            print(f"# Here is our secret : {get_secret()}")
        elif op == "3":
            print(SECRET)
        elif op == "4":
            break
        else:
            print("\n# Please enter the number from the menu.")
    print("\n# Thank you for playing.")
    return 0


if __name__ == "__main__":
    main()
