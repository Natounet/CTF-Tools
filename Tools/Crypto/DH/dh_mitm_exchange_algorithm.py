import pwn
import json
from sympy.ntheory import discrete_log

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# Fonction pour vérifier si un message est correctement paddé en PKCS7
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

# Fonction pour déchiffrer le flag en utilisant le secret partagé, l'IV et le ciphertext
def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Génération de la clé AES à partir du secret partagé en utilisant SHA-1
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    # Conversion de l'IV et du ciphertext de hexadécimal à bytes
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    
    # Déchiffrement du ciphertext en utilisant AES en mode CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    
    # Vérification et suppression du padding PKCS7
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

#

# Connexion au serveur distant
conn = pwn.remote('socket.cryptohack.org', 13379)
banner = conn.recvline()  # Réception de la bannière du serveur

# Négotiation des algorithme d'échange
conn.sendline('{"supported":["DH64"]}')  # Envoi du premier message
response = conn.recvline()  # Réception de la réponse du serveur
conn.sendline('{"chosen": "DH64"}')  # Envoi du second message
message = conn.recvline()  # Réception du message contenant les paramètres d'Alice



alice_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))

p = int(alice_dict['p'], 16)  # Modulus p
g = 2  # Base g (fixée à 2)
A = int(alice_dict['A'], 16)  # Valeur publique A d'Alice

# Comme p est petit (64 bits), on peut retrouver facilement a
# en résolvant le logarithme discret : g^a ≡ A (mod p)
a = discrete_log(p, A, g)

message = conn.recvline()  # Réception du message contenant les paramètres de Bob
bob_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))
B = int(bob_dict['B'], 16)  # Valeur publique B de Bob
b = discrete_log(p, B, g)  # Calcul de b en résolvant le logarithme discret

# Calcul du secret partagé : A^b mod p
secret = pow(A, b, p)

message = conn.recvline()  # Réception du message contenant l'IV et le ciphertext
message_dict = json.loads(message[message.find(b'{'):message.find(b'}') + 1].decode('utf-8'))

# Déchiffrement et affichage du flag
print(decrypt_flag(secret, message_dict['iv'], message_dict['encrypted_flag']))

# Fermeture de la connexion
conn.close()