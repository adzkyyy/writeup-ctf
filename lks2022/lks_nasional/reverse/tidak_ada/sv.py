enc = [0xb3,0xb4,0xac,0xb1,0x84,0x97,0x9e,0x93,0x90,0xa0,0x9e,0x8c,0x9a,0x91,0x98,0xa0,0x9b,0xde,0x8c,0x96,0x91,0xde,0x82]
for i in enc:
    print(chr(i^255), end='')

# FLAG : LKSN{halo_aseng_d!sin!}
