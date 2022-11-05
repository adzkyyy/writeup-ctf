from zlib import crc32
import string

checksum = [0xad68e236,
          0x330c7795,
          0x2060efc3,
          0x4366831a,
          0x15d54739,
          0x916b06e7,
          0xf3b61b38,
          0x1b0ecf0b,
          0x916b06e7,
          0x29d6a3e8,
          0x3dd7ffa7,
          0x5767df55,
          0x3dd7ffa7,
          0x6dd28e9b,
          0x1ad5be0d,
          0xfcb6e20c]

for i in checksum:
    for j in string.printable:
        if crc32(j.encode()) == i:
            print(j,end='')

# FLAG : LKSN{h4sh_CRC32}
