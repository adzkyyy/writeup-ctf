from pwn import *
from itertools import permutations

p = process(["python3", "fastcrypt.py"])

def inp(iv):
    p.sendlineafter(b">> ",b"1")
    p.sendlineafter(b": ", iv)
    p.sendlineafter(b": ", b"a")
    p.recvuntil(b"|   ")
    return p.recvline().decode().strip()
for i in range(1,9):
    exec(f'enc{i} = []')

for i in range(16):
    enc1.append(inp(hex(i).encode()[2:].zfill(2))[2:])
    enc3.append(inp(hex(i).encode()[2:].zfill(4))[4:])
    enc5.append(inp(hex(i).encode()[2:].zfill(6))[6:])
    enc7.append(inp(hex(i).encode()[2:].zfill(8))[8:])

for i in range(0,256,16):
    enc2.append(inp(hex(i).encode()[2:].zfill(2))[2:])
    enc4.append(inp(hex(i).encode()[2:].zfill(4))[4:])
    enc6.append(inp(hex(i).encode()[2:].zfill(6))[6:])
    enc8.append(inp(hex(i).encode()[2:].zfill(8))[8:])

def ngeset(x):
    r = ""
    a = [i for i in set(x)]
    for i in x:
        if i == a[0]:
            r += "0"
        elif i == a[1]:
            r += "1"
    return r

#print(ngeset(enc2))
r = []
for i in range(1,9):
    exec(f"r.append(ngeset(enc{i}))")

print([i for i in r])
#for i in range(1,9):
    #exec(f"print(enc{i})")
