f = open('enc.txt','rb').read().decode()
f = [ord(i) for i in f]
enc = f[:len(f)//2]
x = [enc[i]-enc[i-1] for i in reversed(range(len(enc)))][:-1]
x = 'C'+''.join([chr(i) for i in x][::-1])
print(x)
#COMPFEST14{4dler_ch3ccs0me_1s_f4s7er_7h4n_cRC!!_0240f11cc5}
