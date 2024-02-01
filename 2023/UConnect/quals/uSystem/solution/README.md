# uSystem | Pwn

## Proof of Concept
- bisa overflow menggunakan variable buf karena panjangnya tergantung dari password
- bisa atur panjang password dengan kirim ukuran maksimal variable tanpa null
- leak canary, leak libc main + 243 untuk dapet base libc address
- one_gadget to drop shell