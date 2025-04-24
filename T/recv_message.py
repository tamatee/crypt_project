from elgamal import ElgamalDecrypt, load_key
import os

print("DECRYPTION")
private_key = load_key('keys/private_key.txt')
input_filename = input("file_name: ")
ElgamalDecrypt(input_filename, private_key, 'from_decrypted.txt')