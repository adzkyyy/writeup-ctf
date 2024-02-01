from libnum import solve_crt, n2s
from gmpy2 import iroot

exec(open('output.txt').read())

enc_msg = solve_crt([C1,C2,C3,C4,C5,C6],[N1,N2,N3,N4,N5,N6])
nroot = int(iroot(enc_msg, 27)[0])
print(n2s(nroot))

# FLAG : LKSN{wow_modulusnya_b4nyak_,k4mU_p4kai_hasht4d_br0adc4st_att4ck_kah?_atau_sm4ll_cube_root?_selam4t!!!\\(O_O)/}
