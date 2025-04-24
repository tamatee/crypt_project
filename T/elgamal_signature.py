from signature_utils import *
from utils import load_key
from elgamal import ElgamalDecrypt
import pickle
import math

def RWhash(binary_message, key):
    prime, gen, secret_num = key
    block_size = math.floor(math.log2(prime))
    blocks = binary_to_blocks(binary_message, block_size)
    # print(f"Block size: {block_size}")
    # print(f"Binary blocks: {blocks}")

    block_values = binary_blocks_to_int(blocks)
    # print(f"Integer block values: {block_values}")

    H = len(binary_message) % prime
    # print(f"H0 = {H}")
    i = 1
    for b in block_values:
        H = compression_function(H, b, prime)
        # print(f"H{i} = {H}")
        i+=1

    return H

# def ElgamalSignature(binary_path, sender_key):
#     prime, gen, secret_num = sender_key
#     with open(binary_path, 'rb') as f:
#         binary_message = pickle.load(f)
#     RWhash_value = RWhash(binary_message, prime)
#     sig = ElgamalDecrypt(sender_key, RWhash_value, 'signature/signature.dat')
#     return sig

# Example usage
binary_message_source = get_binary_from_file('input/meme.jpg')
binary_message_decrypted = get_binary_from_file('decrypted/output.jpg')
pk = load_key('keys/public_key.txt')

hash_source = RWhash(binary_message_source, pk)
hash_decrypted = RWhash(binary_message_decrypted, pk)

# ElgamalSignature('encrypted/ciphertext.dat', pk)

# print("Source Hash (decimal):", hash_source)
print("Source Hash (hex)\t:", hex(hash_source))
# print("Decrypted Hash (decimal):", hash_decrypted)
print("Decrypted Hash (hex)\t:", hex(hash_decrypted))