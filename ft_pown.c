unsigned long long ft_pown(unsigned long long base, unsigned long long exp) {
    while (exp > 0)
        base *= base;
    return base;
}