from Crypto.Util.number import *
import random


whatisthis = [1]


def just(a,b):
	return whatisthis[a]//(whatisthis[b]*whatisthis[a-b])


def baby(a,b,n):
	gift = 0
	for i in range(n+1):
		if abs(n - 2*i) != 0xd:
			continue
		gift += just(n,i)*pow(a,i)*pow(b,n-i)
	return gift


def algebra(txt):
	with open(txt,"rb") as f:
		m = f.read().strip()
		m = bytes_to_long(m)
		e,p,q = (1 << 0x10)|1,getPrime(0x400),getPrime(0x400)
		f.close()
		return m,e,p,q


def okay():
	u = random.randint(0xa,0x3e8)
	v = random.randint(0xa,0x3e8)
	w = getPrime(random.randint(5,9))
	return u,v,w


def easy(w):
	global whatisthis
	for i in range(1,w+1):
		whatisthis.append(i*whatisthis[-1])


def apanih(n,e,c,x):
	with open("output.txt","w") as f:
		output = f"{n = }\n"
		output += f"{e = }\n"
		output += f"{c = }\n"
		output += f"{x = }\n"
		f.write(output)
		f.close()


def main():
	m,e,p,q = algebra("flag.txt")
	n = p*q
	c = pow(m,e,n)
	u,v,w = okay()
	easy(w)
	x = baby(p*u*7,-(q*v)*3,w)
	apanih(n,e,c,x)


if __name__ == "__main__":
	main()
