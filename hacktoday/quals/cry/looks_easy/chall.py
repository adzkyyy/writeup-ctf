from Crypto.Util.number import *

def Fn(e):
    return 2**(2**e) +1

def txt(txt):
    with open (txt,"rb") as f:
        m = f.read().strip()
        m = bytes_to_long(m)
        p,q,r = getPrime(0x400), getPrime(0x400),getPrime(0x400)
        f.close()
        return m,p,q,r

def abc(a,b,c):
    x,y,z = (a+b), (b+c), (a+c)
    return x,y,z

def stu(s,t,u):
    v,w,x = s*t, t*u, s*u
    return v,w,x

def main():
    m,p,q,r = txt("flag.txt")
    n = p*q*r
    m1,m2,m3 = abc(p,q,r)
    n1,n2,n3 = stu(m1,m2,m3)
    e = Fn(4)
    c = pow(m,e,n)
    with open("output.txt", "w") as f:
        f.write(f"{c = }\n")
        f.write(f"{e = }\n")
        f.write(f"{n1 = }\n")
        f.write(f"{n2 = }\n")
        f.write(f"{n3 = }\n")


if __name__ == "__main__":
  main()

