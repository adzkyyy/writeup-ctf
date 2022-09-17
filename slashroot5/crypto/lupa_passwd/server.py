#!/usr/bin/env python3

from binascii import unhexlify
from Crypto.Cipher import AES
import json
import os
import random
import string

registered_user = [
    {
        "username": "adm1n",
        "password": os.urandom(32)
    }
]

def send(msg):
    msg = json.dumps(msg)
    print(msg)

def generate_pass(iv):
    idx = random.randint(0, len(registered_user)-1)
    x = registered_user[idx]["username"].encode()
    init = list((x * (32//len(x)+1))[:32])
    random.shuffle(init)

    key = os.urandom(16)
    aes = AES.new(key, AES.MODE_ECB)

    value = b""
    for i in range(len(init)):
        b = aes.encrypt(iv)[0]
        c = b ^ init[i]
        value += bytes([c])
        iv = iv[1:] + bytes([c])

    charset = string.printable[:-6]
    result = ""
    for v in value:
        result += charset[v%len(charset)]

    return result

def login(creds):
    user = creds["username"]
    if user == "adm1n":
        flag = open("flag.txt").read()
        send({
            "message": f"Congrats, here's your flag: {flag}"
        })
    else:
        send({
            "message": f"Nothing to see here, {user}"
        })

def change_pass(username, index, iv):
    new_pass = generate_pass(iv)
    registered_user[index] = {
        "username": username,
        "password": new_pass
    }

    send({
        "message": f"Password has been changed. For further information, please contact Administrator."
    })

if __name__ == "__main__":
    while True:
        try:
            inp = input()
            data = json.loads(inp)
            if data["action"] == "login":
                creds = {
                    "username": data["username"],
                    "password": data["password"]
                }
                if creds in registered_user:
                    login(creds)
                else:
                    send({
                        "message": "Wrong username or password."
                    })

            elif data["action"] == "register":
                registered = False
                for i in range(len(registered_user)):
                    if registered_user[i]["username"] == data["username"]:
                        registered = True
                        break
                if not registered:
                    registered_user.append({
                        "username": data["username"],
                        "password": data["password"]
                    })
                    send({
                        "message": "User has been registered."
                    })
                else:
                    send({
                        "message": "User already exist."
                    })

            elif data["action"] == "change_password":
                found = False
                for i in range(len(registered_user)):
                    if registered_user[i]["username"] == data["username"]:
                        found = True
                        iv =  unhexlify(data["iv"])
                        change_pass(data["username"], i, iv)
                        break
                if not found:
                    send({
                        "message": "Username does not exist."
                        })

            else:
                send({
                    "message": "What is this?"
                })

        except Exception as e:
            send({
                    "message": "Something is wrong"
                })
