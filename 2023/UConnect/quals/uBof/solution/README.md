# uBof | Pwn

## Proof of Concept
- buffer overflow dengan jumlah input yang terbatas akan muncul jika pengguna memasukkan input > 50
- ada gap antara rip dengan panjangan input yang harus dimasukkan pengguna, karena input menggunakan fread() yang akan menunggu input pengguna sampai memenuhi ukuran
- karena pie aktif dan ga ada leak address, ga bisa rop
- pake vsyscall di stack yang addressnya statis