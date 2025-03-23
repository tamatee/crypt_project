#include"crypto.h"
unsigned long long ft_fastexpo(unsigned long long base, unsigned long long exp, unsigned long long N)
{
    unsigned long long result = 1;
    base = base % N;
    while (exp > 0) {
        if (exp & 1) result = (result * base) % N;
        exp = exp >> 1;
        base = (base * base) % N;
    }
    return result;
}