from Crypto.Util.number import *
from math import gcd
import string
from functools import reduce
from pwn import *

class LCG:
    def __init__(self, seed,n,a,c):
        self.n = n
        self.a = a
        self.c = c
        self.seed = seed
    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.n
        return self.seed

def crack_c(s,n,a):
    c = (s[1]-s[0] * a) % n
    return n,a,c

def crack_a(s):
    n = (1<<16)+1
    a = (s[2] - s[1]) * inverse(s[1]-s[0],n) % n
    return crack_c(s,n,a)

msg = b"\x00\x00\x00"

p = process("./chall.py")
p.recvuntil(b":")
p.sendline(b"2")
p.recvuntil(b":")
p.sendline(msg)
p.recvuntil(b"encrypted message:")
enc = p.recvline().decode()
exec("enc = " + enc)
n,a,c = crack_a(enc[-3:])
print(n,a,c)

for i in string.printable[:-6]:
    f = i
    lcg = LCG(enc[0] ^ ord(f), n,a,c)
    for j in range(len(enc)-1):
        a = lcg.next() ^ enc[j+1]
        print(a)
    #    if a in string.printable[:-6]:
    #        print(f)
            #f += a
