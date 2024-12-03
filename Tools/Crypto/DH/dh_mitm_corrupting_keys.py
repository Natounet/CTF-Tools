import json
from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

# Configuration de la connexion
host, port = ('socket.cryptohack.org', 13371)
conn = remote(host, port)

# Paramètres de Diffie-Hellman
g = <g>
p = <p>
c = <c>
C = pow(g, c, p)

# Réception des données d'Alice
conn.recv(timeout=2)
message = conn.recv(timeout=2)

# Extraction et décodage de la partie JSON
alice_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))

# Calcul de g^(ac) et modification du message d'Alice
A = int(alice_dict['A'], 16)
alice_dict['A'] = hex(C)

# Envoi du message modifié à Bob
conn.send(json.dumps(alice_dict))
print("g^(ac) envoyé")

# Réception des données de Bob
message = conn.recvline(timeout=2)
bob_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))

# Modification du message de Bob
B = int(bob_dict['B'], 16)
bob_dict['B'] = hex(C)

# Envoi du message modifié à Alice
conn.send(json.dumps(bob_dict))
print("g^(bc) envoyé")

# Réception du message d'Alice
message = conn.recvline(timeout=2)
message_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))

# Récupération du shared secret
shared_secret = pow(A, c, p)
print(decrypt_flag(shared_secret, message_dict['iv'], message_dict['encrypted_flag']))

# Fermeture de la connexion
conn.close()
