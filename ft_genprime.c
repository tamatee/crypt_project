#include "crypto.h"
// static void byte_to_binary_string(unsigned char byte, char *out)
// {
//     for (int i = 7; i >= 0; i--) {
//         int bit = (byte >> i) & 1;
//         *out++ = bit ? '1' : '0';
//     }
//     *out = '\0';
// }

// static unsigned long long ft_getnum(const char *filename, int n)
// {
//     FILE *fp = fopen(filename, "rb");
//     if (!fp)
//     {
//         perror("Error opening file");
//         return 0;
//     }

//     // Find the file size
//     fseek(fp, 0, SEEK_END);
//     long file_size = ftell(fp);
//     fseek(fp, 0, SEEK_SET);

//     if (file_size <= 0)
//     {
//         fclose(fp);
//         fprintf(stderr, "Empty or invalid file.\n");
//         return 0;
//     }

//     // Read the entire file into a buffer
//     unsigned char *bytes = (unsigned char *)malloc(file_size);
//     if (!bytes)
//     {
//         fclose(fp);
//         fprintf(stderr, "Memory allocation failed.\n");
//         return 0;
//     }

//     size_t read_count = fread(bytes, 1, file_size, fp);
//     fclose(fp);

//     if (read_count != (size_t)file_size)
//     {
//         free(bytes);
//         fprintf(stderr, "Could not read entire file.\n");
//         return 0;
//     }

//     /*
//      * We'll convert each byte to an 8-character binary string => total length = file_size * 8.
//      * Then we’ll combine them into one big string "res".
//      * If you really want the same behavior as `Integer.toBinaryString(b)` for each byte,
//      * you’d have to replicate the sign-extension logic. The below approach is standard 8-bit representation.
//      */
//     size_t max_bits = (size_t)file_size * 8;
//     char *res = (char *)malloc(max_bits + 1); // +1 for '\0'
//     if (!res)
//     {
//         free(bytes);
//         fprintf(stderr, "Memory allocation failed.\n");
//         return 0;
//     }
//     res[0] = '\0';

//     // Build the big binary string
//     for (int i = 0; i < file_size; i++)
//     {
//         // Convert one byte to "XXXXXXXX" (8 bits) and append
//         char temp[9]; // 8 bits + null terminator
//         byte_to_binary_string(bytes[i], temp);
//         strcat(res, temp);
//     }
//     free(bytes);

//     // Now we may need to pad or truncate 'res' to length n
//     size_t res_len = strlen(res);
//     if (res_len < (size_t)n)
//     {
//         // pad with '0' until length == n
//         printf("Before padding: %s\n", res);
//         char *pad_str = (char *)malloc(n + 1);
//         if (!pad_str)
//         {
//             free(res);
//             fprintf(stderr, "Memory allocation failed.\n");
//             return 0;
//         }
//         strcpy(pad_str, res);
//         for (size_t i = res_len; i < (size_t)n; i++)
//         {
//             pad_str[i] = '0';
//         }
//         pad_str[n] = '\0';
//         free(res);
//         res = pad_str;
//     }
//     else if (res_len > (size_t)n)
//     {
//         // truncate
//         res[n] = '\0';
//     }

//     printf("Bit from file: %s\n", res);

//     unsigned long long val = strtoull(res, NULL, 2);
//     free(res);

//     return (long long)val;
// }

// static unsigned long long ft_findprime(unsigned long long num, unsigned long long max)
// {
//     if (num % 2 == 0)
//         num++;

//     while (ft_isprime(num))
//     {
//         if (num > max)
//         {
//             printf("ERROR OUT OF RANGE\n");
//             exit(1);
//         }
//         else
//             num += 2;
//     }
//     return num;
// }

// unsigned long long ft_genprime(const char *filename, int n)
// {
//     unsigned long long num = ft_getnum(filename, n);
//     printf("num: %llu\n", num);

//     if (num % 2 != 0 && ft_isprime(num))
//         printf("Prime number: %llu\n", num);
//     else
//         printf("ERROR: Not a Prime number: %llu\n", num);

//     num = ft_findprime(num, ft_pown(2, n) - 1);
//     printf("Next Prime number: %llu\n", num);
//     return num;
// }

unsigned long long ft_genprime(int bitLength, const char *filename)
{
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "File cannot be opened: %s\n", filename);
        return 0ULL;
    }

    int byteCount = (bitLength + 7) / 8;
    unsigned char *buffer = (unsigned char *)malloc(byteCount);
    if (!buffer) {
        fclose(fp);
        fprintf(stderr, "Memory allocation failed.\n");
        return 0ULL;
    }

    // Read from file
    size_t readCount = fread(buffer, 1, byteCount, fp);
    fclose(fp);

    if (readCount < (size_t)byteCount) {
        // Not enough bytes were read; we can still proceed but will have fewer random bits
        fprintf(stderr, "Warning: requested %d bytes, but only %zu were read.\n",
                byteCount, readCount);
    }

    // Combine the bytes into a 64-bit number
    unsigned long long num = 0ULL;
    for (int i = 0; i < (int)readCount; ++i) {
        num = (num << 8) | buffer[i];
    }
    free(buffer);

    // Enforce top bit to ensure at least 2^(bitLength-1)
    unsigned long long minVal = 1ULL << (bitLength - 1);
    // Maximum is (1 << bitLength) - 1, e.g. for 10 bits => 1023
    unsigned long long maxVal = (1ULL << bitLength) - 1ULL;

    // Force highest bit, mask out extras
    num |= minVal;
    num &= maxVal;

    // Make sure it's odd
    if ((num & 1ULL) == 0ULL) {
        num++;
    }

    // Search for prime in [num..maxVal], stepping by 2
    while (num <= maxVal) {
        if (ft_isprime(num)) {
            printf("Generated Prime: %llu\n", num);
            return num;
        }
        num += 2ULL;  // check only odd numbers
    }

    fprintf(stderr, "No prime found in range.\n");
    return 0ULL;
}