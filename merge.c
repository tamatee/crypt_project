#include <stdbool.h>
#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>

unsigned long long ft_pown(unsigned long long base, unsigned long long exp)
{
    while (exp > 0)
        base *= base;
    return base;
}

unsigned long long ft_ullrandom()
{
    HCRYPTPROV hProv;
    unsigned long long num;

    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT))
    {
        printf("CryptAcquireContext failed!\n");
        exit(1);
    }

    if (!CryptGenRandom(hProv, sizeof(num), (BYTE *)&num))
    {
        printf("CryptGenRandom failed!\n");
        exit(1);
    }

    CryptReleaseContext(hProv, 0);
    return num;
}

unsigned long long ft_gcd(unsigned long long a, unsigned long long b)
{
    while (b != 0)
    {
        a = b;
        b = a % b;
    }
    return a;
}

unsigned long long ft_findinverse(unsigned long long a, unsigned long long mod)
{
    if (mod == 1ULL)
        return 0ULL;

    unsigned long long m0 = mod;
    long long b2 = 0, b1 = 1;

    while (a > 1ULL)
    {
        unsigned long long q = a / mod;

        unsigned long long t = mod;
        mod = a % mod;
        a = t;

        // t = b2
        t = (unsigned long long)b2;

        // b2 = b1 - q * b2
        b2 = b1 - (long long)q * b2;
        // b1 = t
        b1 = (long long)t;
    }

    if (b1 < 0)
    {
        b1 += (long long)m0;
    }

    return (unsigned long long)b1;
}

unsigned long long ft_fastexpo(unsigned long long base, unsigned long long exp, unsigned long long N)
{
    unsigned long long result = 1;
    base = base % N;
    while (exp > 0)
    {
        if (exp & 1)
            result = (result * base) % N;
        exp = exp >> 1;
        base = (base * base) % N;
    }
    return result;
}

bool ft_isprime(unsigned long long n)
{
    if (n <= 1 || n % 2 == 0)
        return false;
    int t = 100;
    while (t > 0)
    {
        unsigned long long a = 2 + ft_ullrandom() % (n - 3);
        unsigned long long r = ft_fastexpo(a, (n - 1) / 2, n);
        if (r != 1 && r != n - 1)
            return false;
    }
    return true;
}

unsigned long long ft_genprime(int bitLength, const char *filename)
{
    FILE *fp = fopen(filename, "rb");
    if (!fp)
    {
        fprintf(stderr, "File cannot be opened: %s\n", filename);
        return 0ULL;
    }

    int byteCount = (bitLength + 7) / 8;
    unsigned char *buffer = (unsigned char *)malloc(byteCount);
    if (!buffer)
    {
        fclose(fp);
        fprintf(stderr, "Memory allocation failed.\n");
        return 0ULL;
    }

    // Read from file
    size_t readCount = fread(buffer, 1, byteCount, fp);
    fclose(fp);

    if (readCount < (size_t)byteCount)
    {
        // Not enough bytes were read; we can still proceed but will have fewer random bits
        fprintf(stderr, "Warning: requested %d bytes, but only %zu were read.\n",
                byteCount, readCount);
    }

    // Combine the bytes into a 64-bit number
    unsigned long long num = 0ULL;
    for (int i = 0; i < (int)readCount; ++i)
    {
        num = (num << 8) | buffer[i];
    }
    free(buffer);

    // Enforce top bit to ensure at least 2^(bitLength-1)
    unsigned long long minVal = 1ULL << (bitLength - 1);
    // Maximum is (1 << bitLength) - 1, e.g. for 10 bits => 1023
    unsigned long long maxVal = (1ULL << bitLength) - 1ULL;

    // Force highest bit, mask out extras
    num |= minVal;
    num &= maxVal;

    // Make sure it's odd
    if ((num & 1ULL) == 0ULL)
    {
        num++;
    }

    // Search for prime in [num..maxVal], stepping by 2
    while (num <= maxVal)
    {
        if (ft_isprime(num))
        {
            printf("Generated Prime: %llu\n", num);
            return num;
        }
        num += 2ULL; // check only odd numbers
    }

    fprintf(stderr, "No prime found in range.\n");
    return 0ULL;
}

void randNowithInverse(unsigned long long n)
{
    srand(time(0));
    unsigned long long e;
    do
    {
        e = ft_ullrandom() % (n - 2) + 2; // e in range [2, n-1]
    } while (ft_gcd(e, n) != 1);

    unsigned long long inv = ft_findinverse(e, n);
    printf("e: %llu\ne^-1 mod n: %llu\nn: %llu\n", e, inv, n);
}

int main()
{
    srand(time(0));

    int bitLength = 10;
    const char *filename = "randomdata.bin"; // Create a binary file with random data

    // Example: Generate prime number from file
    unsigned long long prime = ft_genprime(bitLength, filename);

    // Generate e, e^-1, n
    if (prime != 0)
    {
        randNowithInverse(prime);
    }

    // Overflow check
    printf("\nMaximum value of unsigned long long: %llu\n", ULLONG_MAX);
    printf("Bit size: %d bits\n", sizeof(unsigned long long) * 8);

    return 0;
}