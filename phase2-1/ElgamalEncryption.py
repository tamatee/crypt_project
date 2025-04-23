import random
import sympy
import os
import pickle

def modinv(a, m):
    return pow(a, -1, m)

def generate_large_prime(bits):
    return sympy.randprime(2**(bits-1), 2**bits)

def save_key(file_path, key_data):
    with open(file_path, 'wb') as f:
        pickle.dump(key_data, f)

def load_key(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def ElgamalKeyGen(key_size=128):
    p = generate_large_prime(key_size)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)  # private key
    h = pow(g, x, p)

    private_key = (p, g, x)
    public_key = (p, g, h)

    save_key('keys/private_key.txt', private_key)
    save_key('keys/public_key.txt', public_key)
    print("Keys generated and saved in 'keys/' folder.")
    return private_key, public_key

def ElgamalEncrypt(public_key, input_path):
    p, g, h = public_key

    with open(input_path, 'rb') as f:
        plaintext_bytes = f.read()

    ciphertext = []
    for byte in plaintext_bytes:
        m = byte
        y = random.randint(1, p - 2)
        c1 = pow(g, y, p)
        s = pow(h, y, p)
        c2 = (m * s) % p
        ciphertext.append((c1, c2))

    with open('encrypted/ciphertext.dat', 'wb') as f:
        pickle.dump(ciphertext, f)
    print("File encrypted and saved as 'encrypted/ciphertext.dat'")

def ElgamalDecrypt(private_key, ciphertext_file, output_path):
    p, g, x = private_key

    with open(ciphertext_file, 'rb') as f:
        ciphertext = pickle.load(f)

    plaintext_bytes = bytearray()
    for c1, c2 in ciphertext:
        s = pow(c1, x, p)
        s_inv = modinv(s, p)
        m = (c2 * s_inv) % p
        plaintext_bytes.append(m)

    with open(output_path, 'wb') as f:
        f.write(plaintext_bytes)
    print(f"File decrypted and saved as '{output_path}'")

if __name__ == '__main__':
    os.makedirs('keys', exist_ok=True)
    os.makedirs('encrypted', exist_ok=True)
    os.makedirs('decrypted', exist_ok=True)

    # รับชื่อไฟล์จากผู้ใช้
    input_filename = input("Enter input filename (e.g., input/message.txt): ")
    output_filename = input("Enter output filename for decrypted file (e.g., decrypted/output_message.txt): ")

    # Generate keys
    private_key, public_key = ElgamalKeyGen()

    # Encrypt file
    ElgamalEncrypt(public_key, input_filename)

    # Decrypt file
    ElgamalDecrypt(private_key, 'encrypted/ciphertext.dat', output_filename)
