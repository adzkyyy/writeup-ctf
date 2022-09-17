#!/usr/bin/env python3
from fastecdsa import curve
import hashlib
import random

DESTINASI = {
    "canggu": "terkenal dengan pantai yang sejuk dan ombak selancar",
    "ubud": "terkenal dengan pemandangan alam yang sangat indah",
    "citayam": "terkenal dengan " + open("flag.txt").read(),
}


class Healing:
    def __init__(self):
        self.c = curve.P256
        self.d = random.randint(2, self.c.q - 2)
        self.Q = self.c.G * self.d
        self.k = random.randint(2, self.c.q - 2)
        self.a = random.randint(100, 999)
        self.b = random.randint(100, 999)

    @staticmethod
    def sig2ticket(sig):
        return f"{sig[0]:x}z{sig[1]:x}"

    @staticmethod
    def ticket2sig(ticket):
        try:
            x = ticket.split("z")
            return (int(x[0], 16), int(x[1], 16))
        except:
            print("Tiket kamu rusak")
            exit()

    def refresh(self):
        self.k = (self.a * self.k + self.b) % self.c.q

    def beli_tiket(self, dest: bytes):
        self.refresh()
        z = int(hashlib.sha256(dest).hexdigest(), 16)
        R = self.k * self.c.G
        r = R.x % self.c.q
        s = pow(self.k, -1, self.c.q) * (z + r * self.d) % self.c.q
        return self.sig2ticket((r, s))

    def berangkat(self, dest: bytes, ticket: str):
        r, s = self.ticket2sig(ticket)
        z = int(hashlib.sha256(dest).hexdigest(), 16)
        u1 = z * pow(s, -1, self.c.q) % self.c.q
        u2 = r * pow(s, -1, self.c.q) % self.c.q
        R = u1 * self.c.G + u2 * self.Q
        return r == R.x


def user_input(s=""):
    inp = input(s).strip().lower()
    assert len(inp) < 2048
    return inp


def banner():
    print("Kamu merasa lelah CTFan dan butuh healing? Tenang.")
    print("Kami menyediakan tiket destinasi healing terbaik untukmu.")
    print("\nTiket destinasi healing yang tersedia:")
    print("\n".join(f"[*] {x.title()}" for x in DESTINASI))
    print("\nOpsi:\n[1] Beli tiket\n[2] Berangkat")


def main():
    banner()
    healing = Healing()

    for _ in range(4):
        opt = user_input("\n> ")

        if opt == "1":
            dest = user_input("Destinasi: ")
            assert dest in DESTINASI
            if dest == "citayam":
                print(f"Maaf, tiket ke {dest.title()} sudah habis")
                continue
            ticket = healing.beli_tiket(dest.encode())
            print("Tiket:", ticket)

        elif opt == "2":
            dest = user_input("Destinasi: ")
            assert dest in DESTINASI
            ticket = user_input("Tiket: ")
            res = healing.berangkat(dest.encode(), ticket)
            if res:
                print(f"Tiket ke {dest.title()} terverifikasi, selamat menikmati healingmu")
                print(f"{dest.title()} {DESTINASI[dest]}")
                break
            else:
                print(f"Tiket ke {dest.title()} milikmu rusak")

        else:
            print("?")
            break


if __name__ == "__main__":
    main()
