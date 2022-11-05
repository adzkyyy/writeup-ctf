from Crypto.Util.number import *

p = getPrime(1024)
q = getPrime(1024)
r = p + q
s = p - q
e = 65537
m = open("flag.txt","r").read()
c = pow(bytes_to_long(m.encode()),e,p*q)
print("p+q = ",str(r))
print("p-q = ", str(s))
print("c = "+str(c))