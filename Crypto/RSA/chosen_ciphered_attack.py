import socket
from Crypto.Util.number import bytes_to_long

"""
This script performs an RSA decryption attack using an oracle.

The script connects to a specified server to perform the attack and uses the RSA public key parameters (e, n) and ciphertext (c) to compute an intermediate ciphertext (cprime). It then simulates the oracle's response to this intermediate ciphertext to retrieve the original message.

Functions and Variables:
- ip, port: The IP address and port of the server hosting the oracle.
- e, n: The public exponent and modulus of the RSA key.
- c: The ciphertext to be decrypted.
- cprime: The intermediate ciphertext computed using the oracle attack.
- m2: The simulated response from the oracle, representing the decrypted intermediate ciphertext.
- m: The original message obtained by decoding the oracle's response.
- m_bytes: The original message in bytes.

# Note: The recv/send of messages may need to be modified depending on the specific functioning of the oracle.
# Some oracles may require specific formatting or additional steps for communication.
# Ensure to adjust the recv/send logic as per the oracle's requirements.

Steps:
1. Define the connection parameters and RSA keys.
2. Compute the intermediate ciphertext (cprime) using the oracle attack.
3. Simulate the oracle's response (m2) to the intermediate ciphertext.
4. Decode the oracle's response to retrieve the original message.
"""

# Define connection parameters and RSA keys
(ip, port) = (<host>, <port>)
(e, n) = (<e>, <n>)
c = <c>

# Compute cprime using the oracle attack
cprime = (c * pow(2, e, n)) % n
print(f"cprime: {cprime}")

# Connect to the oracle server and send cprime
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.recv(1024)
    s.sendall(f"{cprime}\n".encode())
    
    # Receive the response from the oracle
    response = s.recv(4096)

    m2 = int(response.decode().strip())
    print(f"m2: {m2}")

# Decode the response to obtain the original message
m = m2 // 2
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
print(f"Decrypted message: {m_bytes}")
