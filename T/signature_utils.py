from utils import FastExpo
def binary_to_blocks(binary_str, block_size):
    blocks = [binary_str[i:i + block_size] for i in range(0, len(binary_str), block_size)]
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0')
    return blocks

def binary_blocks_to_int(blocks):
    return [int(b, 2) for b in blocks]

def compression_function(prev_hash, block_value, prime):
    # print(f"prev_hash: {prev_hash} block_value: {block_value} p: {p}")
    A = prev_hash + block_value
    # print(f"A: {A}")
    B = FastExpo(A, 2, prime)
    # print(f"B: {B}")
    C = (B << 2) % prime
    # print(f"C: {C}")
    return C

def get_binary_from_file(filepath):
    with open(filepath, 'rb') as file:
        byte_data = file.read()
    bit_string = ''.join(format(byte, '08b') for byte in byte_data)
    return bit_string