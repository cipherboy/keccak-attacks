#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint16_t ***matrix;

#ifndef width
    #define width 5000
#endif

void m_init() {
    matrix = calloc(width, sizeof(uint16_t **));
    for (size_t i = 0; i < width; i++) {
        matrix[i] = calloc(width, sizeof(uint16_t *));
        for (size_t j = 0; j < width; j++) {
            matrix[i][j] = calloc(5, sizeof(uint16_t));
        }
    }
}

void m_record(uint8_t a, size_t a_offset, uint8_t b, size_t b_offset) {
    for (size_t i = 0; i < 8; i++) {
        uint8_t _a = a & b;
        uint8_t _b = a & (~b);
        uint8_t _c = (~a) & b;
        uint8_t _d = a ^ b;
        uint8_t _e = a | b;

        for (size_t j = 0; j < 8; j++) {
            size_t jj = 7 - j;
            size_t ii = ((i + jj) % 8);
            matrix[ii+a_offset][jj+b_offset][0] += (_a >> j)&1;
            matrix[ii+a_offset][jj+b_offset][1] += (_b >> j)&1;
            matrix[ii+a_offset][jj+b_offset][2] += (_c >> j)&1;
            matrix[ii+a_offset][jj+b_offset][3] += (_d >> j)&1;
            matrix[ii+a_offset][jj+b_offset][4] += (_e >> j)&1;
        }

        a = (a << 1ull) | ((uint8_t)a >> (uint8_t)(8ull - 1ull));
    }
}

void m_record_arr(uint8_t *a, uint8_t *b) {
    for (size_t a_offset = 0; a_offset < width/8; a_offset++) {
        for (size_t b_offset = 0; b_offset < width/8; b_offset++) {
            m_record(a[a_offset], a_offset*8, b[b_offset], b_offset*8);
        }
    }
}

void m_print() {
    for (size_t k = 0; k < 5; k++) {
        // printf("Function k=%zu:\n[", k);
        printf("[");
        for (size_t i = 0; i < width; i++) {
            printf("[");
            for(size_t j = 0; j < width; j++) {
                printf("%u", matrix[i][j][k]);
                if (j+1 < width) {
                    printf(",");
                }
            }
            printf("]");
            if (i + 1 < width) {
                printf(",\n");
            }
        }
        printf("],\n");
    }
}
