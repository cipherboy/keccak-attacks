#include "matrix.h"
#include "sha3.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <syscall.h>
#include <unistd.h>

static inline void rand_read_raw(uint8_t *output) {
    FILE *fp = fopen("/dev/urandom", "r");
    size_t i = 0;

    if (!fp) {
        perror("rand getter");
        exit(-1);
    }

    for (i = 0; i < 255; i++) {
        output[i] = fgetc(fp);
    }

    fclose(fp);
}


int main() {
    m_init();

    uint8_t rand_data[256];
    size_t rand_index = 256;

    int max_count = 60000;

    printf("[[");
    for (int c = 0; c < max_count; c++) {
        uint8_t data[25];
        uint8_t states[25 * (24 + 1)];
        size_t offset = 0;

        for (size_t i = 0; i < 25; i++) {
            data[i] = 0;
        }

        if (rand_index + 9 > 256) {
            rand_read_raw(rand_data);
            rand_index = 0;
        }
        for (size_t i = 0; i < 9; i++) {
            data[i] = rand_data[rand_index];
            rand_index += 1;
        }

        for (size_t i = 0; i < 25; i++) {
            states[offset*25 + i] = data[i];
        }
        offset += 1;

        State s = create_state(data);

        for (uint32_t round = 0; round < 24; round++) {
            s = keccakf(s, round);
            //printf("Round: %u\n", round);
            //print_state(s, "");
            //printf("\n");
            flaten_state(s, data);
            for (size_t i = 0; i < 25; i++) {
                states[offset*25 + i] = data[i];
            }
            offset += 1;
        }

        printf("[");
        for (int i = 0; i < 25*25; i++) {
            printf("%u", states[i]);
            if (i+1 < 25*25) {
                printf(",");
            }
        }
        printf("]");

        if (c + 1 < max_count) {
            printf(",\n");
        }

        m_record_arr(states, states);
    }
    printf("],\n");
    m_print();
    printf("[]]\n");
}
