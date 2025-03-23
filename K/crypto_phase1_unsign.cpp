#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cmath>
using namespace std;

typedef unsigned long long ULL;
const int TEST_TIMES = 10;

// Function to compute GCD
ULL GCD(ULL a, ULL b) {
    while (b != 0) {
        ULL temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Function to compute modular inverse using Extended Euclidean Algorithm
ULL FindInverse(ULL a, ULL mod) {
    ULL m0 = mod, t, q;
    ULL x0 = 0, x1 = 1;
    if (mod == 1) return 0;
    while (a > 1) {
        q = a / mod;
        t = mod;

        mod = a % mod, a = t;
        t = x0;

        x0 = x1 - q * x0;
        x1 = t;
    }
    if (x1 < 0) x1 += m0;
    return x1;
}

// Fast Exponentiation a^b mod n
ULL FastExpo(ULL a, ULL b, ULL n) {
    ULL result = 1;
    a = a % n;
    while (b > 0) {
        if (b & 1) result = (result * a) % n;
        b = b >> 1;
        a = (a * a) % n;
    }
    return result;
}

// Lehmann primality test
bool IsPrime(ULL n) {
    if (n <= 1 || n % 2 == 0) return false;
    for (int i = 0; i < TEST_TIMES; ++i) {
        ULL a = 2 + rand() % (n - 3);
        ULL r = FastExpo(a, (n - 1) / 2, n);
        if (r != 1 && r != n - 1) return false;
    }
    return true;
}

// Generate random number from file and find prime >= number
ULL GenPrime(int bitLength, const string &filename) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        cerr << "File cannot be opened.\n";
        return 0;
    }

    int byteCount = (bitLength + 7) / 8;
    char *buffer = new char[byteCount];
    file.seekg(0, ios::beg);
    file.read(buffer, byteCount);
    file.close();

    ULL num = 0;
    for (int i = 0; i < byteCount; ++i) {
        num = (num << 8) | (unsigned char)buffer[i];
    }
    delete[] buffer;

    // Align to correct bit length and ensure bitLength-th bit is 1
    ULL minVal = 1ULL << (bitLength - 1);
    ULL maxVal = (1ULL << bitLength) - 1;

    num = num | minVal;  // Ensure highest bit is 1
    num = num & maxVal;  // Ensure not exceeding bit length

    if (num % 2 == 0) ++num;

    while (num <= maxVal) {
        if (IsPrime(num)) {
            cout << "Generated Prime: " << num << endl;
            return num;
        }
        num += 2;  // Only check odd numbers
    }

    cerr << "No prime found in range.\n";
    return 0;
}

// Generate (e, eInverse, n) where gcd(e,n)=1
void GenRandomNoWithInverse(ULL n) {
    srand(time(0));
    ULL e;
    do {
        e = rand() % (n - 2) + 2;  // e in range [2, n-1]
    } while (GCD(e, n) != 1);

    ULL inv = FindInverse(e, n);
    cout << "e: " << e << "\ne^-1 mod n: " << inv << "\nn: " << n << endl;
}

int main() {
    srand(time(0));

    int bitLength = 10;
    string filename = "randomdata.bin";  // Create a binary file with random data

    // Example: Generate prime number from file
    ULL prime = GenPrime(bitLength, filename);

    // Generate e, e^-1, n
    if (prime != 0) {
        GenRandomNoWithInverse(prime);
    }

    // Overflow check
    cout << "\nMaximum value of unsigned long long: " << ULLONG_MAX << endl;
    cout << "Bit size: " << sizeof(ULL) * 8 << " bits\n";

    return 0;
}