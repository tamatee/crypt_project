from signature_utils import *
from utils import load_key
import math

def RWhash(binary_message, p):
    block_size = math.floor(math.log2(p))
    blocks = binary_to_blocks(binary_message, block_size)
    print(f"Block size: {block_size}")
    print(f"Binary blocks: {blocks}")

    block_values = binary_blocks_to_int(blocks)
    print(f"Integer block values: {block_values}")

    H = len(binary_message) % p
    print(f"H0 = {H}")
    i = 1
    for b in block_values:
        H = compression_function(H, b, p)
        print(f"H{i} = {H}")
        i+=1

    return H

# Example usage
binary_message_source = get_binary_from_file('input/meme.jpg')
binary_message_decrypted = get_binary_from_file('decrypted/output.jpg')
pk = load_key('keys/public_key.pem')
p = pk[0]

hash_source = RWhash(binary_message_source, p)
hash_decrypted = RWhash(binary_message_decrypted, p)

print("Source Hash (decimal):", hash_source)
print("Source Hash (hex):", hex(hash_source))
print("Decrypted Hash (decimal):", hash_decrypted)
print("Decrypted Hash (hex):", hex(hash_decrypted))