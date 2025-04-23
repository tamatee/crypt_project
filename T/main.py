import math

from elgamal import ElgamalKeyGen, ElgamalEncrypt, ElgamalDecrypt
from prime import GenPrime, GenerateGenerator

prime = GenPrime('test', 5)
# print(prime)
gen = GenerateGenerator(prime)

# Step 1: Key Generation
private_key, public_key = ElgamalKeyGen(prime, gen)
print("Private Key:", private_key)
print("Public Key:", public_key)

# Step 2: Encryption
plaintext = 15
print("Plaintext: ", plaintext)
ciphertext_a, ciphertext_b = ElgamalEncrypt(plaintext, public_key)
print("Ciphertext A:", ciphertext_a)
print("Ciphertext B:", ciphertext_b)

# Step 3: Decryption
decrypted_message = ElgamalDecrypt(ciphertext_a, ciphertext_b, private_key, public_key[0])
print("Decrypted Message:", decrypted_message)
