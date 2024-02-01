from Crypto.Util.number import *


def push_p(p):
    p += 0xD1CC
    if not p % 0x2:
        p += 0x1
    while not isPrime(p):
        p += 0x2
    return p


def get_factors(nbit):
    p = getPrime(nbit)
    q = push_p(pow(push_p(p), 0x2))
    return (p, q)


def get_modulus(f=()):
    n = 0x1
    for i in f:
        n *= i
    return int(n)


def get_msg(txt):
    with open(txt, "rb") as f:
        m = f.read().strip()
        m = bytes_to_long(m)
        f.close()
        return m


def main():
    factors = get_factors(0x200)
    n = get_modulus(factors)
    m = get_msg("flag.txt")
    e = 0x10001
    c = pow(m, e, n)
    with open("output.txt", "w") as f:
        f.write(f"{n = }\n")
        f.write(f"{e = }\n")
        f.write(f"{c = }\n")
        f.close()


if __name__ == "__main__":
    main()
