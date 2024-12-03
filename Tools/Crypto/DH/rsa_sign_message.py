import Crypto.Hash.SHA256 as SHA256  # Import the SHA256 hashing module from the PyCrypto library

# RSA parameters
n = <n>
d = <d>
m = <m> # The message to be signed

# Create a new SHA256 hash object
hash = SHA256.new()

# Update the hash object with the message encoded to bytes
hash.update(m.encode())

# Compute the RSA signature by raising the hash digest to the power of d modulo n
signature = pow(int.from_bytes(hash.digest(), "big"), d, n)

# Print the computed signature
print(signature)
