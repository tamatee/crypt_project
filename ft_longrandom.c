#include"crypto.h"

long long ft_llrandom() {
    HCRYPTPROV hProv;
    long long num;

    // Acquire cryptographic context
    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
        printf("CryptAcquireContext failed!\n");
        exit(1);
    }

    // Generate random number
    if (!CryptGenRandom(hProv, sizeof(num), (BYTE*)&num)) {
        printf("CryptGenRandom failed!\n");
        exit(1);
    }

    CryptReleaseContext(hProv, 0);
    return num;
}

unsigned long long ft_ullrandom() {
    HCRYPTPROV hProv;
    unsigned long long num;

    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
        printf("CryptAcquireContext failed!\n");
        exit(1);
    }

    if (!CryptGenRandom(hProv, sizeof(num), (BYTE*)&num)) {
        printf("CryptGenRandom failed!\n");
        exit(1);
    }

    CryptReleaseContext(hProv, 0);
    return num;
}