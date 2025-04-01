#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <climits>
using namespace std;

typedef long long LL;
int TEST_TIMES = 100;

// Function to compute GCD
LL GCD(LL a, LL b)
{
    while (b != 0)
    {
        LL temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

LL power(LL base, LL exp) {
        LL res = base;

        while(exp > 1) {
            res *= base;
            exp--;
        }

        return res;
    }

// Function to compute modular inverse using Extended Euclidean Algorithm
LL FindInverse(LL a, LL mod)
{
    LL m0 = mod;
    LL b1 = 1, b2 = 0;
    while (mod > 1)
    {
        LL q = a / mod;
        LL t = mod;
        mod = a % mod;
        a = t;
        t = b2;
        b2 = b1 - q * b2;
        b1 = t;
    }
    if (b2 < 0)
        b2 = (b2 + m0) % m0;
    return b2;
}

// Fast Exponentiation a^b mod n
LL FastExpo(LL a, LL b, LL n)
{
    LL result = 1;
    a = a % n;
    while (b > 0)
    {
        if (b % 2 == 1)
            result = (result * a) % n;
        b /= 2;
        a = (a * a) % n;
    }
    return result;
}

// Lehmann primality test
bool IsPrime(LL n)
{
    srand(time(0));
    LL a = 2 + rand() % (n - 3);
    LL e = (n - 1) / 2;
    int t = TEST_TIMES;
    while (t > 0)
    {
        if (GCD(a, n) > 1)
            return false;
        LL r = FastExpo(a, e, n);
        if ((r % n) == 1 || (r % n) == n - 1)
        {
            a = 2 + rand() % (n - 3);
            t -= 1;
        }
        else
            return false;
    }
    return true;
}

LL getNum(const string &file, int n)
{
    ifstream in(file, ios::binary);
    if (!in.is_open())
    {
        cerr << "File not found: " << file << endl;
        return 0;
    }

    string res;
    char byte;
    while (in.read(&byte, 1))
    {
        unsigned char b = static_cast<unsigned char>(byte);
        res += bitset<8>(b).to_string(); // get 8-bit binary string
    }
    in.close();

    cout << "Bit from File: " << res << endl;

    // Pad or truncate to desired bit length
    if ((int)res.length() < n)
    {
        cout << "Before padding: " << res << endl;
        res.append(n - res.length(), '0');
    }
    else
    {
        res = res.substr(0, n);
    }

    return stoll(res, nullptr, 2); // binary to long long
}

static long findPrime(LL start, LL bound)
{
    if (start % 2 == 0)
        start++;

    while (!IsPrime(start))
    {
        if (start > bound)
        {
            cout << "out of bound" << endl;
            exit(1);
        }
        // System.out.println(start);
        else
            start += 2;
    }
    return start;
}

// Generate random number from file and find prime >= number
LL GenPrime(const string &file, int n)
{
    n %= 33;
    LL num = getNum(file, n);
    cout << "Number from file: " << num << endl;

    if (num % 2 != 0 && IsPrime(num))
    {
        cout << num << " is Prime" << endl;
    }
    else
    {
        cout << num << " is not Prime" << endl;
        num = findPrime(num, power(2, n) - 1);
        cout << "Next Prime is: " << num << endl;
    }

    return num;
}

// Generate (e, eInverse, n) where gcd(e,n)=1
void GenRandomNoWithInverse(LL n)
{
    srand(time(0));
    LL e;
    do
    {
        e = rand() % (n - 2) + 2;
    } while (GCD(e, n) != 1);

    LL inv = FindInverse(e, n);
    cout << "e: " << e << "\ne^-1 mod n: " << inv << "\nn: " << n << endl;
}

int main()
{
    srand(time(0));

    int bitLength = 32;
    string file = "randomdata.bin";

    LL prime = GenPrime(file, bitLength);
    // cout << "power: "<< power(2,2) << endl;
    // cout << "fast: " << FastExpo(28ULL, 13ULL, 143ULL) << endl;
    // cout << "inverse: " << FindInverse(39LL, 11LL) << endl;
    // cout << "is prime: " << IsPrime(prime) << endl;
    // // Generate e, e^-1, n
    if (prime != 0)
    {
        GenRandomNoWithInverse(prime);
    }

    return 0;
}
