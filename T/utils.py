import secrets
import pickle

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

# def get_num(filename, n):
#     with open(filename, 'rb') as file:
#         byte_data = file.read()

#     bit_string = ''.join(format(byte, '08b') for byte in byte_data)
#     # print(bit_string)

#     first_one_index = bit_string.find('1')
#     # print('first_one_index', first_one_index)
#     if first_one_index == -1:
#         return '0' * (n)

#     output_get = bit_string[first_one_index:n]
#     pad_len = n - len(output_get)
#     # print(pad_len)
#     output_get = (output_get, output_get + '0'*pad_len)[pad_len >= 0]
#     print("binary_get: " + output_get + '\nlen: ' + str(len(output_get)))
#     return  int(output_get, 2)

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

def FindInverse(a, m):
    m0 = m
    b1, b2 = 1, 0

    while m > 1:
        q = a // m
        a, m = m, a % m
        b1, b2 = b2, b1 - q * b2

    if b2 < 0:
        b2 = (b2 + m0) % m0

    return b2

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