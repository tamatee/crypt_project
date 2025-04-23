from utils import *
from prime import GenerateGenerator
# Term Project ในส่วนที่ 2.1  เป็นการทำ Elgamal Encryption ค่ะ โดยในโปรแกรมของนักศึกษาอย่างน้อยต้องมี method ต่อไปนี้ (นักศึกษาที่ทำเสร็จแล้ว สามารถสอบพร้อมกับ Project Phase 2.1 ได้เลยค่ะ) 

# ในส่วนนี้ให้นักศึกษาใช้ BigInt ได้เลยค่ะ

# 1. ElgamalKeyGen(???)  method ที่ใช้ในการ Generate public และ private key pair
#     Input : ???
#     Output: ???  private key, public key
# 2. ElgamalEncrypt(???) method ที่ใช้ในการเข้ารหัส  ให้เข้ารหัสได้ทั้งข้อความจากหน้าจอและไฟล์ประเภทต่างๆ
#     Input : key ที่ใช้ในการ...รหัส, Plaintext โดยที่ Plaintext เป็นได้ทั้ง ข้อความที่ได้รับมาจากหน้าจอ หรือ ไฟล์ชนิดต่างๆ
#    Output: Ciphertext file
# 3. ElgamalDecrypt(???) method ที่ใช้ในการถอดรหัสไฟล์ ciphertext
#     Input : key ที่ใช้ในการ...รหัส, Ciphertext file
#    Output: Plaintext file
# -----------------
# นักศึกษาสามารถเพิ่ม method ต่างๆ เพื่อให้โปรแกรมทำงานได้ตามความเหมาะสม
# ??? นักศึกษาคิดพารามิเตอร์เอง
# -----------------

def ElgamalKeyGen(prime):
    secret_num = secrets.randbelow(prime)
    gen = GenerateGenerator(prime)
    y = FastExpo(gen, secret_num, prime)
    private_key = (prime, gen, secret_num)
    public_key = (prime, gen, y)

    save_key('keys/private_key.pem', private_key)
    save_key('keys/public_key.pem', public_key)
    return private_key, public_key

def ElgamalEncrypt(input_path, pk):
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

    with open('encrypted/ciphertext.dat', 'wb') as f:
        pickle.dump(ciphertext, f)
    print("File encrypted and saved as 'encrypted/ciphertext.dat'")

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
    print(f"File decrypted and saved as '{output_path}'")

    return 'decrypted successfully'