import math

from elgamal import ElgamalKeyGen, ElgamalEncrypt, ElgamalDecrypt
from prime import GenPrime, GenerateGenerator

prime = GenPrime(128)

# Step 1: Key Generation
private_key, public_key = ElgamalKeyGen(prime)
print("Private Key:", private_key)
print("Public Key:", public_key)

# Step 2: Encryption
plaintext = 'input/text.txt'
print("Plaintext: ", plaintext)
ciphertext = ElgamalEncrypt(plaintext, public_key)
print("Ciphertext (A,B):", ciphertext)
cipher_path = 'encrypted/ciphertext.dat'

# Step 3: Decryption
decrypted_message = ElgamalDecrypt(cipher_path, private_key, 'decrypted/output.txt')
print("Decrypted Message:", decrypted_message)
