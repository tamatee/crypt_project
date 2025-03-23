long long ft_gcd(long long a, long long b) {
    while (b != 0){
        a = b;
        b = a % b;
    }
    return a;
}