#include <stdio.h>
#include <omp.h>

int main() {
    int current = 1;
    int totalPrimes = 0;
    int threshold = 1000000;
#pragma omp parallel for schedule(dynamic) reduction(+ : totalPrimes)
    for (current = 1; current <= threshold; current++) { 
        int i = 2; 
        while(i <= current) { 
            if(current % i == 0)
                break;
            i++; 
        }
        if(i == current)
            totalPrimes++;
    }
    printf("%d prime numbers under %d\n",totalPrimes,threshold);
    return 0;
}
