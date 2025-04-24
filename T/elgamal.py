import secrets, pickle, math

def get_coprime(p):
    phi = p - 1
    while True:
        k = secrets.randbelow(phi - 1) + 2
        if GCD(k, phi) == 1:
            return k

def GCD(a, b):
    while (b != 0):
        temp = b
        b = a % b
        a = temp
    return a

def get_num(bitlength):
    lower = 2**(bitlength - 1)
    upper = 2**bitlength
    res = secrets.randbelow(upper - lower) + lower
    return res

def FastExpo(base, exp, mod):
    if mod == 0:
        print("Modulo cannot be zero.")
    if exp < 0:
        base = mod_inv(base, mod)
        exp = -exp

    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def mod_inv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        print("No modular inverse for" + str(a) + "mod" + str(m))
    return x % m

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def save_key(file_path, key_data):
    with open(file_path, 'wb') as f:
        pickle.dump(key_data, f)

def load_key(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_signature(file_path, signature):
    with open(file_path, 'wb') as f:
        pickle.dump(signature, f)

def GenPrime(bitlength):
    num = get_num(bitlength)
    if num % 2 != 0 and IsPrime(num) and IsPrime((num - 1) // 2):
        return num
    else:
        prime = find_safe_prime(num)
    return prime

def find_safe_prime(num):
    print('pre-compute: ', num)
    while True:
        if IsPrime(num) and IsPrime((num - 1) // 2):
            break
        else:
            num += 1
    print("safe-prime: ", num)
    print("safe-from: ", (num-1) // 2)
    return num

def IsPrime(num):
    a = secrets.randbelow(num - 3) + 2
    e = (num - 1) // 2
    t = 100
    while(t > 0):
        if (GCD(a, num) > 1):
            return False
        result = FastExpo(a, e, num)
        if((result % num) == 1 or (result % num) == (num - 1)):
            a = secrets.randbelow(num - 3) + 2
            t -= 1
        else:
            return False
    return True

def GenerateGenerator(num):
    a = (num-1) // 2
    gen = secrets.randbelow(num - 2) + 2
    b = FastExpo(gen, a, num)
    print("b:", b, "gen:", gen)
    if b != 1:
        print("Generator: ", gen)
        return gen
    else:
        res = -gen % num
        print("INV-Generator: ", res)
        return res

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

def pack_cipher_and_signature(ciphertext_path, signature_path, output_path="pack/cipherwithsignature"):
    with open(ciphertext_path, 'rb') as f:
        ciphertext = pickle.load(f)

    with open(signature_path, 'rb') as f:
        signature = pickle.load(f)

    package = {
        "ciphertext": ciphertext,
        "signature": signature
    }

    with open(output_path, 'wb') as f:
        pickle.dump(package, f)

    print(f"Ciphertext and signature packed into '{output_path}'")


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

    h = hex(H)
    print(f"Hash value: {h}")
    return h


def ElgamalSignature(input_path, private_key, signature_path='signature/output.sig'):
    prime, gen, x = private_key
    with open(input_path, 'rb') as f:
        message = f.read()

    h = int(RWhash(message, (prime, gen, x)), 16)

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

    h = int(RWhash(message, (prime, gen, 0)), 16)  # secret x not needed for hashing

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

def ElgamalKeyGen(prime):
    secret_num = secrets.randbelow(prime)
    gen = GenerateGenerator(prime)
    y = FastExpo(gen, secret_num, prime)
    private_key = (prime, gen, secret_num)
    public_key = (prime, gen, y)

    save_key('keys/private_key.txt', private_key)
    save_key('keys/public_key.txt', public_key)
    return private_key, public_key

def ElgamalEncrypt(input_path, pk, output_path='encrypted/ciphertext.dat', signature_path='encrypted/output.sig'):
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
    ElgamalSignature(input_path, private_key, signature_path)
    return 'encrypted successfully'

def ElgamalDecrypt(cipher_path, private_key, output_path, signature_path='from_sender/output.sig'):
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
    public_key = load_key('recv_keys/public_key.txt')
    is_valid = ElgamalVerification(output_path, public_key, signature_path)
    print("Signature valid:", is_valid)
    return 'decrypted successfully'