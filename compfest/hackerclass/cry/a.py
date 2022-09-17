import random
from sage.all import *
from pwn import *
from Crypto.Util.number import GCD, long_to_bytes
from hashlib import sha256

TemperingMaskB = 0x9d2c5680
TemperingMaskC = 0xefc60000

def untemper(y):
    y = undoTemperShiftL(y)
    y = undoTemperShiftT(y)
    y = undoTemperShiftS(y)
    y = undoTemperShiftU(y)
    return y

def undoTemperShiftL(y):
    last14 = y >> 18
    final = y ^ last14
    return final

def undoTemperShiftT(y):
    first17 = y << 15
    final = y ^ (first17 & TemperingMaskC)
    return final

def undoTemperShiftS(y):
    a = y << 7
    b = y ^ (a & TemperingMaskB)
    c = b << 7
    d = y ^ (c & TemperingMaskB)
    e = d << 7
    f = y ^ (e & TemperingMaskB)
    g = f << 7
    h = y ^ (g & TemperingMaskB)
    i = h << 7
    final = y ^ (i & TemperingMaskB)
    return final

def undoTemperShiftU(y):
    a = y >> 11
    b = y ^ a
    c = b >> 11
    final = y ^ c
    return final

def gcd(a,b): return a.monic() if b == 0 else gcd(b, a%b)

#def attacc(n, e, pad1, pad2, ct1, ct2):
#    R.<X> = Zmod(n)[]
#    f1 = (X - pad1) ^ e - ct1
#    f2 = (X - pad2) ^ e - ct2
#    return -gcd(f1, f2).coefficients()[0]

def attacc(n, e, pad1, pad2, ct1, ct2):
    R = Zmod(n)['X']; (X,) = R._first_ngens(1)
    f1 = (X + pad1) ** e - ct1
    f2 = (X + pad2) ** e - ct2
    return -gcd(f1, f2).coefficients()[0]

def randoms(rand):
    randbits = [rand.getrandbits(32) << 32 * i for i in reversed(range(0, 6))]
    return randbits[0] | randbits[1] | randbits[2] | randbits[3] | randbits[4] | randbits[5]

p = remote('103.185.38.238',18924)
ct = []

random_output = []

for i in range(104):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b": ")
    j = int(p.recvuntil(b"\n")[:-1].decode('utf-8'), 16)
    random_output.append(int(j >> 160))
    for k in range(4, 0, -1):
        random_output.append(int((j >> (32 * k)) & 0xFFFFFFFF))
    random_output.append(int(j & 0xFFFFFFFF))

rand = random.Random()
recovered_state = (3, tuple([ untemper(v) for v in random_output[:624] ] + [0]), None)
rand.setstate(recovered_state)

for i in range(624):
        assert random_output[i] == rand.getrandbits(32)

pad1 = int(sha256(long_to_bytes(randoms(rand))).hexdigest(), 16)
pad2 = int(sha256(long_to_bytes(randoms(rand))).hexdigest(), 16)
print(pad1, pad2)

p.recvuntil(b"> ")
p.sendline(b"2")

p.recvuntil(b"e: ")
e = int(p.recvuntil(b"\n")[:-1], 16)
print("e: " + hex(e))
p.recvuntil(b"N: ")
N = int(p.recvuntil(b"\n")[:-1], 16)
print("N: " + hex(N) + "\n")

p.recvuntil(b"Your encrypted flag is: ")
ct.append(int(p.recvuntil(b"\n")[:-1], 16))
print("ct_1: " + hex(ct[len(ct) - 1]))

p.recvuntil(b"> ")
p.sendline(b"2")
p.recvuntil(b"Your encrypted flag is: ")
ct.append(int(p.recvuntil(b"\n")[:-1], 16))
print("ct_2: " + hex(ct[len(ct) - 1]))

print(long_to_bytes(int(attacc(N,e,pad1,pad2,ct[0],ct[1]))))
#f = open('out', 'w')
#f.writelines([str(j) + "=" + str(i) + "\n" for j,i in zip(["n", "e", "pad1", "pad2", "ct1", "ct2"], [N,e,pad1,pad2,ct[0],ct[1]])])

p.close()
