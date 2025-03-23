#include"crypto.h"

// for safe gen in Linux
// long long ft_longrandom() {
//     int fd = open("/dev/random", O_RDONLY);
//     long long random;
//     read(fd, &random, sizeof(random));
//     close(fd);
//     return random;
// }

long long ft_longrandom() {
    return ((long long)rand() << 32) | rand();
}

int main()
{
    printf("%lld\n", ft_longrandom());
    printf("Minimum value of long long: %lld\n", LLONG_MIN);
    printf("Maximum value of long long: %lld\n", LLONG_MAX);
}