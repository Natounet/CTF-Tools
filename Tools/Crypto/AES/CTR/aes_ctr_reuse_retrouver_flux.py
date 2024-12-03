import base64
import itertools
import string
from math import log2
from itertools import product
from Crypto.Util.strxor import strxor

# Étape 1 : Chargement et préparation des données

# Charger les ciphertexts
ciphertext_lines = []
with open('ch23/file.txt.crypt', 'r') as file:
    ciphertext_lines = file.read().splitlines()

# Décoder les ciphertexts (base64 -> bytes)
ciphertext_bytes = [base64.b64decode(line) for line in ciphertext_lines]

# Découper les ciphertexts en blocs de 16 octets (AES-128 utilise des blocs de 16 octets)
blocks = []
for c in ciphertext_bytes:
    blocks.extend([c[i:i + 16] for i in range(0, len(c), 16)])

# Définir le jeu de caractères supposé dans le texte en clair
charset = string.printable

# Exclure certains caractères non attendus
excluded_chars = "\n\x0b\x0c\r~`%#$"
for char in excluded_chars:
    charset = charset.replace(char, '')

# Initialiser les ensembles possibles pour chaque octet de la clé
# Chaque position peut prendre n'importe quelle valeur entre 0 et 255 au départ
potential_key_values = [set(range(256)) for _ in range(16)]

# Étape 2 : Réduction de l'espace des clés possibles
# Pour chaque bloc, réduire les ensembles de valeurs possibles pour chaque position de la clé
for block in blocks:
    for i in range(len(block)):
        valid_values = set()
        for value in potential_key_values[i]:
            xor_result = value ^ block[i]  # Calculer l'octet du texte en clair hypothétique
            if chr(xor_result) in charset:  # Vérifier s'il appartient au jeu de caractères
                valid_values.add(value)
        # Mettre à jour l'ensemble des valeurs possibles pour cette position de la clé
        potential_key_values[i].intersection_update(valid_values)

# Calculer le nombre de combinaisons possibles de la clé
num_combinations = 1
for values in potential_key_values:
    num_combinations *= len(values)

# Afficher les résultats
print(f"Nombre de combinaisons possibles de la clé : {num_combinations}")
bits_to_bruteforce = log2(num_combinations)
print(f"Nombre de bits à bruteforcer : {bits_to_bruteforce}")

# Étape 3 : Brute-force pour tester les clés possibles
# Prendre un bloc comme test pour essayer les clés candidates
test_block = blocks[0]

# Générer toutes les combinaisons possibles de la clé à partir des ensembles restreints
for key_index, key_candidate in enumerate(product(*potential_key_values)):
    # Appliquer la clé candidate au bloc pour obtenir le texte en clair
    plaintext = ''.join(chr(b ^ k) for b, k in zip(test_block, key_candidate))
    print(f"Clé candidate #{key_index}: {key_candidate} -> Plaintext: {plaintext}")

# Étape 4 : Déchiffrement complet avec la clé trouvée
# Définir la clé finale supposée trouvée (flux de clé AES pour le nonce donné)
FLUX = (208, 51, 177, 37, 12, 71, 27, 44, 119, 221, 201, 255, 193, 113, 67, 246)

# Déchiffrer chaque ciphertext avec la clé trouvée
for encrypted_line in ciphertext_bytes:
    # Répliquer la clé (flux) autant que nécessaire pour la taille du ciphertext
    num_blocks = len(encrypted_line) // 16 + 1
    full_key = (bytes(FLUX) * num_blocks)[:len(encrypted_line)]
    decrypted_line = strxor(full_key, encrypted_line)
    # Afficher le texte en clair (en ignorant les erreurs de décodage UTF-8)
    print(decrypted_line.decode('utf-8', errors='ignore'))
