#!/usr/bin/env python3

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
n = <n>                                                                  
e = 1
ct = <ct>

# Because e == 1, M == C 



print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

decrypted = long_to_bytes(ct)
print(decrypted)