from Crypto.Util.number import *

def do_gen():
	e = 3
	p = getStrongPrime(2048)
	q = getStrongPrime(2048)
	N = p*q
	msg = open("flag.txt","rb").read()
	c = pow(bytes_to_long(msg),e,N)
	c = pow(c,e,N)
	c = pow(c,e,N)
	return N, c 

with open("output.txt","w") as n:
	for count in range(1,7):
		N, c = do_gen()
		n.write("N"+str(count)+" = "+str(N)+"\n")
		n.write("C"+str(count)+" = "+str(c)+"\n")
	n.close()