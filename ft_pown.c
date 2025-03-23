long long ft_pown(long long base, long long exp) {
    while (exp > 0)
        base *= base;
    return base;
}