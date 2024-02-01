# uNote | Pwn

## Proof of Concept
- free() 4 kali, untuk adjust double free nanti sama leak heap base
- null fd tcache bin, terus malloc lagi. sekarang tcache bin kosong, tapi masih ada count 2
- bikin fake chunks pake size 0x91 biar free ke 8 masuk ke unsorted bin untuk leak libc
- overwrite _free_hook -> system. system('/bin/sh')