#include "crypto.h"
unsigned long long ft_findinverse(unsigned long long a, unsigned long long mod)
{
    unsigned long long m0 = mod, q, t;
    unsigned long long b1 = 1, b2 = 0;
    if (mod == 1)
        return 0;

    while (mod > 1)
    {
        q = a / mod;
        t = mod;
        mod = a % mod;
        a = t;
        t = b2;

        b2 = b1 - q * b2;
        b1 = t;
    }

    if (b2 < 0)
        b2 = b2 + m0;

    return b1;
}