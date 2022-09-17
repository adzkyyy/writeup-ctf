from hashlib import md5
from string import ascii_uppercase as allchar
from itertools import product

has = 'ec5482139fc9c29c206a88f49e89d304'

for i in product(allchar, repeat=4):
    k = ''.join(i).encode()
    h = md5(k).hexdigest()
    if h == has:
        print(k)
