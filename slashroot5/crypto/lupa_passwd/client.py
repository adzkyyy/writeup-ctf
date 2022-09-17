#!/usr/bin/env python3

from getpass import getpass
import json
import os
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9999))

def process(action, username, password="", iv=b""):
    data = {
        "action": action,
        "username": username,
        "iv": iv.hex()
    }

    if action != "change_password":
        data.update({
            "password": password,
        })
    

    final = json.dumps(data).encode()
    s.send(final + b"\n")

    response = json.loads(s.recv(1024).strip())
    print()
    print(response["message"])


if __name__ == "__main__":
    while True:
        print("="*11)
        print("Welcome!")
        print()
        print("[1] Login")
        print("[2] Register")
        print("[3] Change password")
        print("[4] Exit")
        print("="*11)
        print()
        inp = input("Input: ")
        print()

        if inp == "1":
            user = input("Username: ")
            password = getpass()
            process("login", user, password)
        elif inp == "2":
            user = input("Username: ")
            password = getpass()
            confirm_password = getpass(prompt="Confirm Password: ")
            if password == confirm_password:
                process("register", user, password)
            else:
                print("Password does not match.")
        elif inp == "3":
            user = input("Username: ")
            iv = os.urandom(16)
            process("change_password", user, password="", iv=iv)
        elif inp == "4":
            print("Cya...")
            s.close()
            break
        else:
            print("Unknown input...")
        print()
