#include <fstream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main() {
    ofstream file("randomdata.bin", ios::binary);
    srand(time(0));
    for (int i = 0; i < 1; ++i) {  // 128 bytes random
        // char byte = rand() % 256;
        char byte = 1;
        file.write(&byte, 1);
    }
    file.close();
    return 0;
}