#include"crypto.h"
bool ft_isprime(unsigned long long n) {
    if (n <= 1 || n % 2 == 0) return false;
    int t = 100;
    while (t > 0) {
        unsigned long long a = 2 + ft_ullrandom() % (n - 3);
        unsigned long long r = ft_fastexpo(a, (n - 1) / 2, n);
        if (r != 1 && r != n - 1) return false;
    }
    return true;
}