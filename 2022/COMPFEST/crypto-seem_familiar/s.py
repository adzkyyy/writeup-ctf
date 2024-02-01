from pwn import *
import string

p = remote('103.185.38.163',13841)
ln = 96
flag = b""

def ecb(x):
    p.sendlineafter(b"> ",b"2")
    p.sendlineafter(b"(in hex) = ", str(x).encode())
    p.recvuntil(b"(in hex): ")
    return p.recvline(0).strip().decode()

while True:
    # temp for test
    pay = (b'A'* (ln-1)).hex()
    resp = bytes.fromhex(ecb(pay))
    block = [resp[i:i+16] for i in range(0,len(resp),16)]
    
    # actual oracle bruteforce
    for i in string.printable[:-6]:
        payload = pay + flag.hex() + i.encode().hex()
        check = bytes.fromhex(ecb(payload))
        block_check = [check[i:i+16] for i in range(0, len(check),16)]
        if block_check[5] == block[5]:
            flag += i.encode()
            print(flag)
            ln -= 1
            break

p.interactive()
