unsigned long long ft_findinverse(unsigned long long a, unsigned long long mod) {
    unsigned  long long m0 = mod;
    unsigned  long long b1 = 1;
    unsigned  long long b2 = 0;

    while (mod > 1)  {
        unsigned  long long q = a / mod;
        unsigned  long long t = mod;
        mod = a % mod;
        a = t;
        t = b2;
        b2 = b1 - q * b2;
        b1 = t;
    }

    if (b2 < 0)
        (b2 += m0) % m0;

    return b2;
}