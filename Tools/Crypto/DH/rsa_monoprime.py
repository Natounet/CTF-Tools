# Given values
n = <n>                                                                  
e = <e>
ct = <ciphertext>

# Calculate phi (Euler's totient function) for n
# Since n is a prime number, phi(n) = (n-1)*(n-1)
phi = (n-1)*(n-1)

# Calculate the modular inverse of e modulo phi
# This is the private key exponent d
d = pow(e, -1, phi)

# Decrypt the ciphertext using the private key (d, n)
pt = pow(ct, d, n)

# Convert the plaintext number to bytes and decode it to a string
print(int.to_bytes(pt, 128, 'big').decode())
