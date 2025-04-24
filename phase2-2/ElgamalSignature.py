import random
from sympy import isprime, mod_inverse
import os

# Generate ElGamal key pair
def ElgamalKeyGen(bits=256):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            break
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)  # private key
    y = pow(g, x, p)  # public key
    public_key = (p, g, y)
    private_key = x
    return private_key, public_key

# RWHash function
def RWHash(message_bytes, p):
    bin_data = ''.join(f'{byte:08b}' for byte in message_bytes)
    block_size = p.bit_length()
    blocks = [bin_data[i:i+block_size] for i in range(0, len(bin_data), block_size)]
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0')  # padding with zeros
    blocks = [int(b, 2) for b in blocks]
    h = len(bin_data) % p  # Initial H0 is the original message length mod p
    for b in blocks:
        h = ((h + b) ** 2 % p << 2) % p
    return hex(h)

# ElGamal Signature function
def ElgamalSignature(private_key, message_path, public_key):
    p, g, _ = public_key
    with open(message_path, 'rb') as f:
        message = f.read()
    h = int(RWHash(message, p), 16)
    while True:
        k = random.randint(1, p - 2)
        if isprime(k) and mod_inverse(k, p - 1):
            break
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p - 1)
    s = (k_inv * (h - private_key * r)) % (p - 1)
    signature = (r, s)
    with open('signature.txt', 'w') as f:
        f.write(f'{r}\n{s}')
    print("Signature saved to 'signature.txt'")

# ElGamal Signature Verification
def ElgamalVerification(message_path, signature_path, public_key):
    p, g, y = public_key
    with open(message_path, 'rb') as f:
        message = f.read()
    h = int(RWHash(message, p), 16)
    with open(signature_path, 'r') as f:
        r = int(f.readline())
        s = int(f.readline())
    if not (0 < r < p and 0 < s < p - 1):
        return False
    v1 = (pow(y, r, p) * pow(r, s, p)) % p
    v2 = pow(g, h, p)
    return v1 == v2

# Example usage
if __name__ == '__main__':
    priv_key, pub_key = ElgamalKeyGen()
    input_file = input("Enter message filename to sign: ")
    ElgamalSignature(priv_key, input_file, pub_key)
    sig_valid = ElgamalVerification(input_file, 'signature.txt', pub_key)
    print("Signature valid:" if sig_valid else "Invalid signature.")
