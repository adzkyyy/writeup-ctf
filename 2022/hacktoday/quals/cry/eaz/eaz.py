#!/usr/bin/python3

from Crypto.Cipher import AES as AEZ
from os import urandom
from hashlib import md5
import sys


FLAG = open("flag.txt").read()
SIZE = 0x10
KEY = urandom(SIZE)


def pad(txt):
    c = bytes([SIZE - len(txt) % SIZE])
    n = SIZE - len(txt) % SIZE
    return txt + c * n


def unpad(txt):
    return txt[0 : -txt[-1]]


def enkrip(txt):
    txt = md5(txt).digest() + txt + pad(b"notadmin")
    iv = urandom(SIZE)
    aes = AEZ.new(KEY, AEZ.MODE_CBC, iv)
    ct = aes.encrypt(txt)
    return (iv + ct).hex()


def dekrip(txt):
    txt = bytes.fromhex(txt)
    iv = txt[:SIZE]
    txt = txt[SIZE:]

    aes = AEZ.new(KEY, AEZ.MODE_CBC, iv)
    txt = aes.decrypt(txt)
    hazz = txt[:SIZE]
    user = txt[SIZE:-SIZE]
    whois = txt[-SIZE:]
    if md5(user).digest() != hazz:
        print("ERROR!!!")
        exit(1)
    return unpad(user), unpad(whois) == b"admin"


def banner():
    print(
        """
█████████████████████████████████████████████████████████████████
██▀▄─██▄─▄▄▀█▄─▀█▀─▄█▄─▄█▄─▀█▄─▄████▀▄─██▄─▄▄▀█▄─▄▄─██▀▄─██░▄▄░▄█
██─▀─███─██─██─█▄█─███─███─█▄▀─█████─▀─███─▄─▄██─▄█▀██─▀─███▀▄█▀█
▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▀▄▄▀▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀
"""
    )


def menu():
    print(
        """Choose menu:
[1] Login.
[2] Register.
[3] Exit."""
    )


def main():
    banner()
    while True:
        menu()
        opsi = input("> ").strip()
        if opsi == "1":
            cookie = input("Enter your cookie : ").strip()
            user, verified = dekrip(cookie)
            if user == b"admin":
                if not verified:
                    print("Fake admin detected!")
                    break
                print("Welcome, Admin!")
                print(f"Congrats! You got this : {FLAG}\n")
                break
            print(f"You are not admin!, You are {str(user)[2:-1]}.\n")
        elif opsi == "2":
            user = input("Enter your username (in hex) : ")
            user = bytes.fromhex(user)
            user = pad(user)
            if user == pad(b"admin"):
                print("Not allowed!")
                break
            cookie = enkrip(user)
            print(f"Here is your cookie : {cookie}\n")
        elif opsi == "3":
            break


if __name__ == "__main__":
    main()
