# uStats | Pwn

## Proof of Concept
- overflow pada simpan data karena total data dibatasi
- input harus diconvert menjadi double
- bypass canary menggunakan '.'
- harus leak libc biar tau versinya