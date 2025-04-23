#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <climits>
#include <bitset>
#include <vector>
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

LL power(LL base, LL exp)
{
    LL res = base;

    while (exp > 1)
    {
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
        res += bitset<8>(b).to_string(); // แปลงเป็น binary string 8-bit
    }
    in.close();

    cout << "Bit from File: " << res << endl;

    size_t firstOne = res.find('1');
    if (firstOne == string::npos)
    {
        cerr << "No '1' found in file data!" << endl;
        return 0;
    }

    res = res.substr(firstOne);
    // cout << "res  " + res << endl;
    if ((int)res.length() < n)
    {
        cout << "Before padding: " << res << endl;
        res.append(n - res.length(), '0'); // เติม 0 ด้านท้าย
    }
    else
    {
        res = res.substr(0, n);
    }

    LL num = stoll(res, nullptr, 2);

    LL maxVal = (1LL << n) - 1;
    if (num > maxVal)
    {
        cout << "Value exceeded max limit, adjusting..." << endl;
        num = maxVal;
    }

    return num;
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
        else
            start += 2;
    }
    return start;
}

// Generate random number from file and find prime >= number
LL GenPrime(const string &file, int n)
{
    // n %= 33;
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

bool IsSafePrime(LL p)
{
    // Check if p is prime and (p-1)/2 is prime
    if (IsPrime(p) && IsPrime((p - 1) / 2))
    {
        return true;
    }
    return false;
}

LL findGenerator(LL p)
{
    vector<LL> fact;
    LL phi = p - 1, n = phi;
    for (LL i = 2; i * i <= n; ++i)
        if (n % i == 0)
        {
            fact.push_back(i);
            while (n % i == 0)
                n /= i;
        }
    if (n > 1)
        fact.push_back(n);

    // Try random candidates
    for (int attempt = 0; attempt < 100; ++attempt)
    {
        LL res = rand() % (p - 2) + 2; // random in [2, p-1]
        bool ok = true;
        for (LL i = 0; i < fact.size() && ok; ++i)
            ok &= FastExpo(res, phi / fact[i], p) != 1;
        if (ok)
            return res;
    }
    return -1;
}

LL getGenerator(LL p)
{
    if (IsSafePrime(p))
    {
        LL g;
        do
        {
            g = rand() % (p - 1) + 2; // Generate a number in the range [1, p-1]
            cout << "g: " + g << endl;
        } while (FastExpo(g, (p - 1) / 2, p) == 1); // Ensure g is a generator

        return g;
    }
    else
    {
        return FindGenerator(p); // If not a safe prime, return generator from findGenerator
    }
}

LL getGenerator(LL p)
{
    if (IsPrime((p - 1) / 2))
    {
        LL g = rand() % (p - 1) + 2;
        return FastExpo(g, (p - 1) / 2, p);
    }
    else
        return findGenerator(p);
}

int main()
{
    srand(time(0));

    int bitLength = 31;
    string file = "randomdata.bin";

    LL prime = GenPrime(file, bitLength);
    if (prime != 0)
    {
        GenRandomNoWithInverse(prime);
    }

    return 0;
}