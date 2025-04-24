from elgamal import ElgamalKeyGen, ElgamalEncrypt, ElgamalDecrypt
from prime import GenPrime, GenerateGenerator
import os

os.makedirs('signature', exist_ok=True)
key_size = int(input("Enter key size: "))
prime = GenPrime(key_size)
input_filename = input("Enter input filename (e.g., message.txt): ")
output_filename = "decrypted/" + input("Enter output filename for decrypted file (e.g., output_message): ")

# Step 1: Key Generation
os.makedirs('keys', exist_ok=True)
private_key, public_key = ElgamalKeyGen(prime)
print("Private Key:", private_key)
print("Public Key:", public_key)

# Step 2: Encryption && signature generation
os.makedirs('encrypted', exist_ok=True)
ciphertext = ElgamalEncrypt(input_filename, public_key)
print("Ciphertext (A,B):", ciphertext)
cipher_path = 'encrypted/ciphertext.dat'

# Step 3: Decryption && signature verification
os.makedirs('decrypted', exist_ok=True)
decrypted_message = ElgamalDecrypt(cipher_path, private_key, output_filename)
print("Decrypted Message:", decrypted_message)