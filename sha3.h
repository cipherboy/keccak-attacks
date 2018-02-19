/*
 * SHA-3 permutation function implementation (Keccak-p)
 * Copyright (C) 2018 Alexander Scheel
 *
 * Implemented from FIPS 202
*/

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <inttypes.h>
#include <assert.h>

#define l 3
#define b (25*(1 << l))
#define w (b/25)
#define inttype uint8_t
#define PRIit PRIu8

#define State inttype**

inttype rotr(inttype x, inttype shift) {
    return (x >> shift) | (x << (w - shift ));
}

State new_state() {
    State s = calloc(5, sizeof(inttype *));
    assert(s != NULL);

    for (size_t i = 0; i < 5; i++) {
        s[i] = calloc(5, sizeof(inttype));
        assert(s[i] != NULL);
    }

    return s;
}

State copy_state(State in) {
    State cpy = new_state();

    for (size_t i = 0; i < 5; i++) {
        for (size_t j = 0; j < 5; j++) {
            cpy[i][j] = in[i][j];
        }
    }

    return cpy;
}

void print_state(State s, char *name) {
    for (size_t i = 0; i < 5; i++) {
        for (size_t j = 0; j < 5; j++) {
            printf("%s[%zu][%zu] = %" PRIit "\n", name, i, j, s[i][j]);
        }
    }
    printf("\n");
}

State keccaktheta(State in, uint32_t round) {
    inttype *C = calloc(5, sizeof(inttype));
    inttype *D = calloc(5, sizeof(inttype));
    State out = new_state();
    for (size_t x = 0; x < 5; x++) {
        C[x] = in[x][0] ^ in[x][1] ^ in[x][2] ^ in[x][3] ^ in[x][4];
    }
    for (size_t x = 0; x < 5; x++) {
        D[x] = C[(x + 4) % 5] ^ rotr(C[(x + 1) % 5], 1);
    }
    for (size_t x = 0; x < 5; x++) {
        for (size_t y = 0; y < 5; y++) {
            out[x][y] = in[x][y] ^ D[x];
        }
    }

    return out;
}

State keccakrho(State in, uint32_t round) {
    State out = copy_state(in);
    size_t x = 1;
    size_t y = 0;
    for (size_t t = 0; t <= 23; t++) {
        out[x][y] = rotr(in[x][y], ((t+1)*(t+2))/2 % w);
        x, y = y, (2*x + 3*y) % 5;
    }

    return out;
}

State keccakpi(State in, uint32_t round) {
    State out = copy_state(in);
    for (size_t x = 0; x < 5; x++) {
        for (size_t y = 0; y < 5; y++) {
            out[x][y] = in[(x + 3*y) % 5][x];
        }
    }

    return out;
}

State keccakchi(State in, uint32_t round) {
    State out = copy_state(in);
    for (size_t x = 0; x < 5; x++) {
        for (size_t y = 0; y < 5; y++) {
            out[x][y] = in[x][y] ^ ((~in[(x+1) % 5][y]) & in[(x+2) % 5][y]);
        }
    }

    return out;
}

inttype keccakrc(uint32_t t) {
    if ((t % 255) == 0) {
        return 1;
    }

    uint16_t r = 1;

    for (size_t i = 1; i < (t % 255) + 1; i++) {
        r = (r << 1);
        r = r ^ (((r >> 8) & 1) << 0);
        r = r ^ (((r >> 8) & 1) << 4);
        r = r ^ (((r >> 8) & 1) << 5);
        r = r ^ (((r >> 8) & 1) << 6);
        r = r & 255;
    }

    return (inttype)(r&1);
}

inttype keccakrcinttype(uint32_t round) {
    inttype r = 0;
    inttype o = 0;
    for (size_t j = 0; j <= l; j++) {
        o = keccakrc(j + 7*round);
        r = r | (o << ((1 << j) - 1));
    }
    return r;
}

State keccakiota(State in, uint32_t round) {
    State out = copy_state(in);
    out[0][0] = in[0][0] ^ keccakrcinttype(round);
    return out;
}

State keccakf(State in, uint32_t round) {
    State int1 = keccaktheta(in, round);
    State int2 = keccakrho(int1, round);
    State int3 = keccakpi(int2, round);
    State int4 = keccakchi(int3, round);
    State int5 = keccakiota(int4, round);
    return int5;
}

State keccakp(State in) {
    State s = copy_state(in);
    for (uint32_t i = 0; i < 24; i++) {
        keccakf(s, i);
    }
    return s;
}
