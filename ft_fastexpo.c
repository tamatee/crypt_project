#include"crypto.h"
#include<stdio.h>
void ft_fastexpo(unsigned long long base, unsigned long long exp, unsigned long long N)
{
    unsigned long long result = 1ULL;
    base = base % N;
    while (exp > 0)
    {
        if (exp % 2 == 1)
            result = (result * base) % N;
        exp = exp >> 1;
        base = (base * base) % N;
    }
}