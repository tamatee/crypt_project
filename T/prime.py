from utils import *

def GenPrime(filename, bitlength):
    num = get_num(filename, bitlength)
    if num % 2 != 0 and IsPrime((num - 1) // 2):
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
    if FastExpo(gen, a, num) != 1:
        print("Generator: ", gen)
        return gen
    else:
        print("Generator: ", gen)
        return -gen % num