long long ft_findinverse(long a, long mod) {
    long long m0 = mod;
    long long b1 = 1;
    long long b2 = 0;

    while (mod > 1)  {
        long long q = a / mod;
        long long t = mod;
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