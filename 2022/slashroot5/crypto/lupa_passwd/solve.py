from pwn import *
import json
import string

context.log_level = "warn"
found = True
while found:
    r = process("./server.py")
    r.sendline('{"action":"register","username":"A","password":"kosong"}')
    r.recvline()
    data = {"action":"change_password","username":"adm1n","iv":"00"*64}
    r.sendline(json.dumps(data))
    r.recvline()
    for i in string.printable[:-6]:
        data = {"action":"login","username":"adm1n","password":i*32}
        r.sendline(json.dumps(data))
        tmp = json.loads(r.recvline().strip())
        if 'Wrong' not in tmp['message']:
            print(tmp['message'])
    r.close()
