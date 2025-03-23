#include"crypto.h"
unsigned long long ft_fastexpo(unsigned long long base, unsigned long long exp, unsigned long long N)
{
    unsigned long long result = 1ULL;
    while (exp > 0)
    {
        if (exp % 2 == 0)
            result = (result * base) % N;
        base = (base * base) % N;
        exp /= 2;
    }
    
}