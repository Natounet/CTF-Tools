import base64
import itertools

def xor_bytes(b1, b2):
    """
    Effectue un XOR entre deux bytes.
    :param b1: Bytes 1
    :param b2: Bytes 2
    :return: Résultat du XOR sous forme de liste d'octets
    """
    return [x ^ y for x, y in zip(b1, b2)]

def check_xor(xors, word):
    """
    Vérifie où un mot supposé pourrait apparaître dans un XOR donné.
    :param xors: Liste d'octets représentant le résultat du XOR
    :param word: Mot à tester
    :return: Liste des correspondances possibles
    """
    word_bytes = [ord(c) for c in word]
    results = []

    # Tester le mot à toutes les positions possibles
    for i in range(len(xors) - len(word_bytes) + 1):
        segment = xors[i:i + len(word_bytes)]
        guessed_text = "".join([chr(c ^ w) for c, w in zip(segment, word_bytes)])
        
        # Vérifier si le texte deviné contient uniquement des caractères valides
        if all(c.isalnum() or c.isspace() for c in guessed_text):  # Lettres, chiffres, espaces
            results.append((guessed_text, i))
    
    return results

# Données chiffrées encodées en Base64
ciphers_base64 = []
with open('ch23/file.txt.crypt', 'r') as file:
    ciphers_base64 = file.read().splitlines()

# Décoder les chaînes en bytes
ciphers = [base64.b64decode(c) for c in ciphers_base64]

# Calculer tous les XOR possibles entre paires de ciphers
xor_results = {}
for (i, c1), (j, c2) in itertools.combinations(enumerate(ciphers), 2):
    xor_results[(i, j)] = xor_bytes(c1, c2)

# Tester le mot "the" à toutes les positions
known_word = "The Jargon File contains a bunch of definitions of the term"
found_words = []  # Collecter les résultats trouvés

for (i, j), xor in xor_results.items():
    matches = check_xor(xor, known_word)
    for guessed_text, position in matches:
        found_words.append((guessed_text, i, j, position))

# Afficher uniquement les mots valides trouvés
print("Mots trouvés :")
for word, cipher1, cipher2, pos in found_words:
    print(f"Mot : '{word}' trouvé entre les ciphers {cipher1} et {cipher2} à la position {pos}")

# If you want
# The basic d
# y call them
# There is an expert program
# The hacker 
# You can val
# There is a 
# The Jargon 
# What Is a Hacker
# tions of the
# and writers have
# cRYPTOaLWAysF
# they call themsel
# You can validate the challenge with the
# If you want to be a hacker
# There is another group of people 
# The basic difference is the
# The Jargon File contains a bunch of d
# There is another group of people who call 
# There is another group of people who loudly call themself 
# The Jargon File contains a bunch of definitions of the term 
# There is a communication
# and phreaking t
# you can find it If you want to
# and the earlies
# ditions of the sha

import base64

# Données fournies
plaintext_known = "The Jargon File contains a bunch of definitions of the term"

# Décodage des ciphers
cipher1 = ciphers[1]
cipher2 = ciphers[7]

# Extraire le flux de clé à partir de cipher1 et du texte clair connu
keystream = bytes([c ^ p for c, p in zip(cipher1, plaintext_known.encode())])

# Utiliser le flux de clé pour déchiffrer cipher2
plaintext2 = bytes([c ^ k for c, k in zip(cipher2, keystream)])

# Affichage des résultats
print("Keystream (hex):", keystream.hex())
print("Plaintext extrait de cipher2 :", plaintext2.decode(errors="replace"))
