from utils import *
from prime import GenerateGenerator
from elgamal_signature import ElgamalSignature, ElgamalVerification

def ElgamalKeyGen(prime):
    secret_num = secrets.randbelow(prime)
    gen = GenerateGenerator(prime)
    y = FastExpo(gen, secret_num, prime)
    private_key = (prime, gen, secret_num)
    public_key = (prime, gen, y)

    save_key('keys/private_key.txt', private_key)
    save_key('keys/public_key.txt', public_key)
    return private_key, public_key

def ElgamalEncrypt(input_path, pk, output_path='encrypted/ciphertext.dat'):
    prime, generator, y = pk

    with open(input_path, 'rb') as f:
        plaintext_bytes = f.read()

    ciphertext = []
    for byte in plaintext_bytes:
        m = byte
        k = get_coprime(prime)
        cipher_text_a = FastExpo(generator, k, prime)
        cipher_text_b = FastExpo(y, k, prime) * m % prime
        ciphertext.append((cipher_text_a, cipher_text_b))

    with open(output_path, 'wb') as f:
        pickle.dump(ciphertext, f)
    print(f"File encrypted and saved as {output_path}")

    private_key = load_key('keys/private_key.txt')
    ElgamalSignature(input_path, private_key, 'signature/output.sig')

    return 'encrypted successfully'

def ElgamalDecrypt(cipher_path, private_key, output_path):
    prime, generator, u = private_key

    with open(cipher_path, 'rb') as f:
        cipher_bytes = pickle.load(f)

    plaintext_bytes = bytearray()
    for cipher_bytes_a, cipher_bytes_b in cipher_bytes:
        a_inv = FastExpo(cipher_bytes_a, u, prime)
        s = FastExpo(a_inv, -1, prime)
        m = (cipher_bytes_b * s) % prime
        plaintext_bytes.append(m)

    with open(output_path, 'wb') as f:
        f.write(plaintext_bytes)
    print(f"File decrypted and saved as {output_path}")
    public_key = load_key('keys/public_key.txt')
    is_valid = ElgamalVerification(output_path, public_key, 'signature/output.sig')
    print("Signature valid:", is_valid)
    return 'decrypted successfully'