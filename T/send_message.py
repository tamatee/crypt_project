from elgamal import ElgamalEncrypt, load_key
import os

print("ENCRYPTION")
public_key = load_key('recv_keys/public_key.txt')
input_filename = input("file_name: ")
os.makedirs('encrypted', exist_ok=True)
os.makedirs('signature', exist_ok=True)
ciphertext = ElgamalEncrypt(input_filename, public_key, output_path='encrypted/image_cipher.dat')
print("Ciphertext (A,B):", ciphertext)