import os
from elgamal import GenPrime, ElgamalKeyGen
os.makedirs('signature', exist_ok=True)
key_size = int(input("Enter key size: "))
prime = GenPrime(key_size)

# Step 1: Key Generation
os.makedirs('keys', exist_ok=True)
private_key, public_key = ElgamalKeyGen(prime)
print("Private Key:", private_key)
print("Public Key:", public_key)