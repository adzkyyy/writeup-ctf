# uCalc | Pwn

## Proof of Concept
- memcpy() overflow varible store
- isi stored_result dengan 0 jadi saat free() dipanggil program ga segfault meskipun overflow
- rop untuk dapetin shell