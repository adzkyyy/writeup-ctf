import this

solper = open("flag.txt.malware","rb").read()

placeholder_1 = ""
for content in range(len(solper)):
	placeholder_1 += chr(solper[content] ^ ord(this.s[content % len(solper)]))

for i in placeholder_1:
	print(chr(ord(i) ^ 2 ^ 3 ^ 7 ^ 9 ^ 11 ^13),end="")

# FLAG : LKSN{w4h_kamU_b!sa_84hasa_uLar_yang_diG0reng_a.k.a_PYC}
