#include"crypto.h"
bool ft_isprime(unsigned long long n) {
    unsigned long long a = ft_ullrandom() + 2;

    unsigned long long e = (n - 1) / 2;

    int t = 100;

    while (t > 0)
    {
        if (ft_gcd(a, n) > 1)
            return false;
        unsigned long long res = ft_fastexpo(a, e, n);
        if ((res % n) == 1 || (res % n) == (n - 1))
        {
            a = ft_ullrandom() + 2;
            t--;
        }
        else
        {
            return false;
        }
    }
    return true;
}