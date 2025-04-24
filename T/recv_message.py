from elgamal import ElgamalDecrypt
from utils import load_key
import os

print("DECRYPTION")
public_key = load_key('keys/private_key.txt')
input_filename = input("file_name: ")
os.makedirs('encrypted', exist_ok=True)
ciphertext = ElgamalEncrypt(input_filename, public_key, output_path='encrypted/from_ciphertext.dat')
print("Ciphertext (A,B):", ciphertext)