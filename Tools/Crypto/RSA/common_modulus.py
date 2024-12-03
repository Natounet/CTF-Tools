from Crypto.PublicKey import RSA
import base64



# Requirement for the attack
#  - Two public keys (e1, n) and (e2, n) with a common modulus n
#  - Two ciphertexts c1 and c2 encrypted with the public keys
#  - The same message m was encrypted with both public keys
#  PGCD(e1, e2) = 1
#  PGCD(c2, n) = 1

def read_public_key(pem_path):
    with open(pem_path, 'r') as pem_file:
        key = RSA.import_key(pem_file.read())
    return (key.e, key.n)

def read_ciphertext(cipher_path):
    with open(cipher_path, 'r') as cipher_file:
        ciphertext = base64.b64decode(cipher_file.read().strip())
    return int.from_bytes(ciphertext, byteorder='big')

def extended_gcd(e1, e2):
    if e1 == 0:
        return e2, 0, 1
    gcd, x1, y1 = extended_gcd(e2 % e1, e1)
    a = y1 - (e2 // e1) * x1
    b = x1
    return gcd, a, b
    

def common_modulus_attack(e1,e2,c1,c2,n):
    gcd, a, b = extended_gcd(e1, e2)
    if gcd != 1:
        raise ValueError("e1 and e2 are not coprime")
    if extended_gcd(c2, n)[0] != 1:
        raise ValueError("c2 and n are not coprime")

    # Compute c1^a * c2^b mod n
    part1 = pow(c1, a, n)
    part2 = pow(c2, b, n)
    message = (part1 * part2) % n

    return message



(e1, n) = read_public_key("key1_pub.pem")
(e2, n) = read_public_key("key2_pub.pem")
c1 = read_ciphertext("message1")
c2 = read_ciphertext("message2")
m = common_modulus_attack(e1,e2,c1,c2,n)

print(bytearray.fromhex(hex(m)[2:]).decode())
