from pwn import *

f = open('ct.hex','r').read().strip()
block = [f[i:i+32] for i in range(0, len(f), 32)]
r = remote('challenge.nahamcon.com',30769)

def xsor(s1, s2):
    x = xor(bytes.fromhex(s1), bytes.fromhex(s2))
    return ''.join(['{:02x}'.format(i) for i in x])

def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(
            ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "")
            + (hex(i + 1).split("0x")[1]))
    return "00" * (size_block - (i + 1)) + "".join(l)

def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split("0x")[1]
    return "00" * (size_block - (i + 1))+ ("0" if len(hex_char) % 2 != 0 else "")+ hex_char+ "".join(l)

def valid(ch, i):
    res = []
    f = xsor(ch, i)
    res.insert(0, f)
    return res

# flag = 'flag{0b1a83a2f3d2836b5059c31166c97f6f}'
for x in reversed(range(1, len(block))):
    val = []
    for j in range(16):
        for i in range(0x0, 0xff):
            if len(val) <= 0:
                val.insert(0, '')

            r.sendlineafter(b'Choice: ', b'0'),
            pad = block_search_byte(16,j,i,val)
            cip = pad.encode() + block[x].encode()
            bp = block_padding(16,j)
            r.sendlineafter(b'(hex): ', cip)
            if r.recvline().strip() == b'valid':
                k = xsor(bp, pad)
                res = valid(k[-(2*(j+1)):], '{:02x}'.format(j+2))
                val = res
                #print(f'trying pad = {hex(i)}')
                m = xsor(k, block[x-1])
                print("plain = ", bytes.fromhex(m))
                break

r.interactive()