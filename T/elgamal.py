from utils import *
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

def ElgamalKeyGen(prime, gen):
    sk = secrets.randbelow(prime)
    y = FastExpo(gen, sk, prime)
    pk = (prime, gen, y)
    return sk, pk

def ElgamalEncrypt(m, pk):
    k = get_coprime(pk[0])
    cipher_text_a = FastExpo(pk[1], k, pk[0])
    cipher_text_b = FastExpo(pk[2], k, pk[0]) * m % pk[0]
    return cipher_text_a, cipher_text_b

def ElgamalDecrypt(a, b, sk, prime):
    a_inv = FastExpo(a, sk, prime)
    s = FastExpo(a_inv, -1, prime)
    plaintext = (b * s) % prime
    return plaintext