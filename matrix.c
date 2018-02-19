#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint32_t ***matrix;
#define addr(_x, _y) ((_x)*64 + _y)

void init() {
    matrix = calloc(64, sizeof(uint32_t **));
    for (size_t i = 0; i < 64; i++) {
        matrix[i] = calloc(64, sizeof(uint32_t *));
        for (size_t j = 0; j < 64; j++) {
            matrix[i][j] = calloc(5, sizeof(uint32_t));
        }
    }
}

void record(uint64_t a, uint64_t b) {
    for (size_t i = 0; i < 64; i++) {
        uint64_t _a = a & b;
        uint64_t _b = a & (~b);
        uint64_t _c = (~a) & b;
        uint64_t _d = a ^ b;
        uint64_t _e = a | b;

        for (size_t j = 0; j < 64; j++) {
            matrix[i][j][0] += (_a >> j)&1;
            matrix[i][j][1] += (_b >> j)&1;
            matrix[i][j][2] += (_c >> j)&1;
            matrix[i][j][3] += (_d >> j)&1;
            matrix[i][j][4] += (_e >> j)&1;
        }

        a = (a << 1) | (a >> (64 - 1));
    }
}

void print() {
    for (size_t k = 0; k < 5; k++) {
        printf("Function k=%zu:\n[", k);
        for (size_t i = 0; i < 64; i++) {
            printf("[");
            for(size_t j = 0; j < 64; j++) {
                printf("%u,", matrix[i][j][k]);
            }
            printf("],");
        }
        printf("]\n\n");
    }
}

int main() {
    printf("Initializing...\n");
    init();
    printf("Single...\n");
    uint64_t a[10] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09};
    uint64_t b[10] = {~0xF0ull, ~0xF1ull, ~0xF2ull, ~0xF3ull, ~0xF4ull, ~0xF5ull, ~0xF6ull, ~0xF7ull, ~0xF8ull, ~0xF9ull};
    for (size_t j = 0; j < 1000; j++) {
        for (size_t i = 0; i < 625; i++) {
            record(a[1], b[0]);
        }
    }

    printf("Printing...\n");
    print();

    return 0;
}
