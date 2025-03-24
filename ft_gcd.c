#include"crypto.h"
unsigned long long ft_gcd(unsigned long long a, unsigned long long b) {
    while (b != 0){
        a = b;
        b = a % b;
    }
    return a;
}