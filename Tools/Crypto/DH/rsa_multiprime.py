import requests

# RSA parameters
n = <n>
e = <e>
ct = <ciphertext>

def factorize_number(number):
    # Query FactorDB API to factorize the number
    url = f"http://factordb.com/api?query={number}"
    response = requests.get(url)
    data = response.json()
    
    # Check if the factorization was successful
    if data['status'] == 'FF':
        return data['factors']
    else:
        return None

phi = 1
# Get the prime factors of n
factors = [factor[0] for factor in factorize_number(n)]
    
# Calculate phi (Euler's totient function) for n
# Since n is a product of multiple primes, phi(n) = (p1-1)*(p2-1)*(p3-1)*...
for factor in factors:
    phi *= (int(factor)-1)

# Calculate the modular inverse of e modulo phi
# This is the private key exponent d
d = pow(e, -1, phi)

# Decrypt the ciphertext using the private key exponent d
cc = pow(ct, d, n)

# Convert the decrypted integer to bytes and decode to get the plaintext message
print(int.to_bytes(cc, 128, 'big').decode())
