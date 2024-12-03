
# Analysis and Flag Extraction from a `.PYC` File

## 1. Identifying the File Format

Using the `file` command on the provided file, we get the following information:
```
Byte-compiled Python module for CPython 3.11, timestamp-based, .py timestamp: Thu Nov 28 19:48:37 2024 UTC, .py size: 1978 bytes
```

The file is identified as a `.PYC` file, which contains compiled Python code.

## 2. Decompiling the File

To recover readable Python code, the `PYCDC` tool can be used: [PYCDC on GitHub](https://github.com/zrax/pycdc).  
This process provides an obfuscated Python script. After deobfuscating, the following logic is obtained:

```python
import base64
import zlib
import marshal
import random

# Global variable
upup = None

# Function to perform calculations and decompress a string
def compute_rand(string):
    global upup
    (a, b, c) = (42, 3.14, -7)
    
    # Perform arbitrary calculations
    result = ((a ** 2 + b ** 0.5) * c) % 13 + (a & int(b))
    result = round((b / 3.14) ** (c + 10), 5)
    
    # Decompress the provided string
    upup = zlib.decompress(base64.b64decode(string))
    
    # Return a random integer
    return random.randint(1, 100)

# Function to retrieve and decode a flag
def get_flag(upup):
    data = 'AMSI{aGFoYWhhX25vdF9kb25lX3lldF9tYW4=}'.encode('utf-8')
    
    # Obfuscated lambdas to process data
    encoded = b''.join([bytes([byte ^ 0xFF]) for byte in data])  # XOR (example placeholder logic)
    decoded = base64.b64decode(encoded)
    
    upup = 7
    return decoded.strip(b'AMSI').strip(b'')

# Loader function to run the challenge
def loader():
    global upup
    print('Starting the challenge...')
    
    # Compute random value with a Base64-encoded and zlib-compressed string
    compute_rand(
        'eJxtkc9LG0EUx2cTI9hdUvx56EFGb5GSFVEwKgVpC3qwggl4XMbZZ7JkM7PMvD2sGujRY28eSq8i9J/ZlBxkwZP0L/C2J2f9rTi892Xee583M4+5Ji/WiPFJ4zdHRs6Ib/UJWs9lv3Ruor9Pmb51YvnlbqnYqyksvyBHTshv8ucNbxGfNMkrrvIeURv9kX/a3GluH0cJ9wLtiUX0sLPc8raWld/P578LBEWxA7QLCUVJYxFK3r3LHIasvUazD7sRiCZo1oN85qtUCjjO0dYDQAO9RvPpfSVFuzijTlsqoazNAjFXK2WVQEQxZpVIBQJNbGvgCtArWrOy4XUxM6X5ituRPXC7LAzcb5LHPRCoXfNqKVwEjW4bBCiG4B0kRrj0oR4l2UfGMWahdxgLjoEU+eITB4KrJELw7+ENMxcL9Zf6m44xc7/eM/KTXM4sndpX1cl0anVQbQyrjdPypV399fmfPZvas1fOeDqxerFuxNjAaQydRvpo/4tibeAsDJ2F9NFuio+4BVBtm2s='
    )
    
    # Execute obfuscated/marshaled code
    marshaled_code = marshal.loads(b'...')  # Replace with actual marshaled bytecode
    exec(marshaled_code)
    
    # Reset upup
    upup = None

# Dummy function to confuse decompilers
def confuse_decompiler():
    junk_code = [
        (lambda: print("Analyzing this won't help.")),
        (lambda: random.choice([
            'Flag not here!',
            'Still nothing here...'
        ])),
    ]
    for func in junk_code:
        func()

loader()
```

## 3. Retrieving the Flag

By analyzing the `compute_rand()` function, it is clear that the decryption process involves Base64 decoding followed by 7z decompression of the input string.  
The variable `upup` contains the result of this process. By printing this variable, we can extract the flag:

```python
print(upup)
```

Example output:
```
b'\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x13\x00\x00\x00\xf3z\x00\x00\x00\x97\x00d\x01}\x00t\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x02\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00}\x01|\x01d\x03k\x02\x00\x00\x00\x00r\x14t\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x04|\x00\x9b\x00\x9d\x02\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x00S\x00t\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x05\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x00S\x00)\x06N\xfa\x1aAMSI{pyc_is_n0t_th4T_H4rd}\xfa"Enter the key to unlock the flag: \xda\nOpenSesame\xfa\x16Correct! The flag is: \xfa\x15Wrong key. Try again!)\x02\xda\x05input\xda\x05print)\x02\xda\x0bsecret_flag\xda\x03keys\x02\x00\x00\x00  \xfa5/home/kali/Documents/pycon/test/generate_byte_code.py\xda\x0factual_function\xfa0generate_encrypted_code.<locals>.actual_function\t\x00\x00\x00sR\x00\x00\x00\x80\x00\xd8\x162\x88\x0b\xdd\x0e\x13\xd0\x148\xd1\x0e9\xd4\x0e9\x88\x03\xd8\x0b\x0e\x90,\xd2\x0b\x1e\xd0\x0b\x1e\xdd\x0c\x11\xd0\x128\xa8;\xd0\x128\xd0\x128\xd1\x0c9\xd4\x0c9\xd0\x0c9\xd0\x0c9\xd0\x0c9\xe5\x0c\x11\xd0\x12)\xd1\x0c*\xd4\x0c*\xd0\x0c*\xd0\x0c*\xd0\x0c*\xf3\x00\x00\x00\x00'
```

The flag is:
```
AMSI{pyc_is_n0t_th4T_H4rd}
```
