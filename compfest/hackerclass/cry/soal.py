#!/usr/bin/env python3
from Crypto.Util.number import getStrongPrime, long_to_bytes,bytes_to_long
from random import getrandbits
from hashlib import sha256
#from secret import FLAG
FLAG = bytes_to_long(b'Do you really think LCG with RSA will make secure system btw flag is GLUG{n44m_l3k3_k44m_4151_50urc3_73r3_bh41_k1}' + b'A'*10)
p = getStrongPrime(1024)
q = getStrongPrime(1024)
N = p * q
e = 3
def get_flag():
    return pow(FLAG + getrandbits(50) , e, N)

print(long_to_bytes(getrandbits(50)))
print(f'e = {e}')
print(f'N = {N}')
print(f'c1 = {get_flag()}')
print(f'c2 = {get_flag()}')
