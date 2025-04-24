from signature_utils import *
from utils import load_key, mod_inv, FastExpo, save_signature, get_coprime
import secrets
import pickle
import math

def RWhash(binary_message, key):
    prime, gen, secret_num = key
    block_size = math.floor(math.log2(prime))

    if isinstance(binary_message, bytes):  # convert bytes to bit string
        binary_message = ''.join(format(b, '08b') for b in binary_message)

    blocks = binary_to_blocks(binary_message, block_size)
    block_values = binary_blocks_to_int(blocks)

    H = len(binary_message) % prime
    for b in block_values:
        H = compression_function(H, b, prime)

    return H


def ElgamalSignature(input_path, private_key, signature_path='signture/sig.'):
    prime, gen, x = private_key

    with open(input_path, 'rb') as f:
        message = f.read()

    h = RWhash(message, (prime, gen, x))

    k = get_coprime(prime)

    r = FastExpo(gen, k, prime)
    k_inv = FastExpo(k, -1, prime - 1)  # or use modinv(k, prime - 1)
    s = (k_inv * (h - x * r)) % (prime - 1)

    signature = (r, s)
    save_signature(signature_path, signature)
    print(f"Signature saved to {signature_path}")
    return signature

def ElgamalVerification(input_path, public_key, signature_path):
    prime, gen, y = public_key
    r, s = load_key(signature_path)

    with open(input_path, 'rb') as f:
        message = f.read()

    h = RWhash(message, (prime, gen, 0))  # secret x not needed for hashing

    if not (0 < r < prime):
        return False

    v1 = (FastExpo(y, r, prime) * FastExpo(r, s, prime)) % prime
    v2 = FastExpo(gen, h, prime)

    return v1 == v2

# Example usage
# binary_message_source = get_binary_from_file('text.txt')
# binary_message_decrypted = get_binary_from_file('decrypted/text.txt')
# pk = load_key('keys/public_key.txt')

# hash_source = RWhash(binary_message_source, pk)
# hash_decrypted = RWhash(binary_message_decrypted, pk)

# print("Source Hash (hex)\t:", hex(hash_source))
# print("Decrypted Hash (hex)\t:", hex(hash_decrypted))

# ElgamalSignature("text.txt", load_key('keys/private_key.txt'), "signature/output.sig")

# is_valid = ElgamalVerification("decrypted/text.txt", load_key("keys/public_key.txt"), "signature/output.sig")
# print("Signature valid:", is_valid)