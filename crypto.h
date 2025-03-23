#include<stdbool.h>
#include<windows.h>
#include<wincrypt.h>
#include<stdio.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>

unsigned long long ft_gcd(unsigned long long a, unsigned long long b);
unsigned long long ft_inversegcd(unsigned long long a, unsigned long long b, unsigned long long c);
// unsigned long long ft_llrandom();
unsigned long long ft_ullrandom();
unsigned long long ft_fastexpo(unsigned long long base, unsigned long long exp, unsigned long long N);
bool ft_isprime(unsigned long long n);
unsigned long long ft_genprime(int bitLength, const char *filename);