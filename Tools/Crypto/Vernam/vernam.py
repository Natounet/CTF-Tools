def vernam_cipher(text, key, mode="encrypt"):
    """
    Generalized Vernam cipher function for encryption and decryption.

    Parameters:
    - text (str): The input text to encrypt or decrypt.
    - key (list): A list of integers serving as the cipher key.
    - mode (str): "encrypt" for encryption or "decrypt" for decryption.

    Returns:
    - str: The resulting encrypted or decrypted text.
    """
    if len(text) != len(key):
        raise ValueError("The length of the text and key must be the same.")
    
    # Complete alphabet to ensure proper operation
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []

    for i in range(len(text)):
        if text[i] not in alphabet:
            raise ValueError(f"Character '{text[i]}' is not in the alphabet.")
        
        # Get the index shift based on the mode
        if mode == "encrypt":
            shift = (alphabet.index(text[i]) + key[i]) % len(alphabet)
        elif mode == "decrypt":
            shift = (alphabet.index(text[i]) - key[i]) % len(alphabet)
        else:
            raise ValueError("Mode must be either 'encrypt' or 'decrypt'.")

        # Append the resulting character to the result list
        result.append(alphabet[shift])

    return "".join(result)

# Example usage:
text = "APPLE"
key = [1, 4, 2, 3,7]

# Encrypt
encrypted_text = vernam_cipher(text, key, mode="encrypt")
print("Encrypted text:", encrypted_text)

# Decrypt
decrypted_text = vernam_cipher(encrypted_text, key, mode="decrypt")
print("Decrypted text:", decrypted_text)
