from signature_utils import binary_to_blocks, binary_blocks_to_int, compression_function
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
binary_message = '11011010110100100101001001001001110100111111111011'
p = 3001
final_hash = RWhash(binary_message, p)
print("Final Hash (decimal):", final_hash)
print("Final Hash (hex):", hex(final_hash))