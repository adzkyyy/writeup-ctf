import os

with open('secretFile.txt', 'r') as f:
	text = f.read()

flag = len(text)

for i in range (flag):
    txt = 'secretFile'
    txt += str(i)
    txt += '.txt'
    with open(txt, 'w') as f:
        f.write(text[i])

