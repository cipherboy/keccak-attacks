#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <assert.h>

uint32_t *u_point;
uint32_t *u_rank;
uint32_t u_disjoint;
uint32_t u_size;

bool *u_parent;
uint32_t *u_sizes;
bool u_changed;

void ufds_init(uint32_t n) {
    u_point = calloc(n, sizeof(uint32_t));
    u_rank = calloc(n, sizeof(uint32_t));
    u_parent = malloc(n * sizeof(bool));
    for (size_t i = 0; i < n; i++) {
        u_point[i] = i;
        u_parent[i] = true;
    }

    u_size = n;
    u_sizes = NULL;
    u_disjoint = n;
    u_changed = true;
}

uint32_t ufds_find(uint32_t i) {
    if (u_point[i] == i) {
        return i;
    }

    uint32_t r = ufds_find(u_point[i]);
    u_point[i] = r;
    return r;
}

int ufds_is_same(uint32_t i, uint32_t j) {
    return ufds_find(i) == ufds_find(j);
}

void ufds_union(uint32_t i, uint32_t j) {
    if (!ufds_is_same(i, j)) {
        u_changed = true;
        uint32_t x = ufds_find(i);
        uint32_t y = ufds_find(j);

        if (u_rank[x] > u_rank[y]) {
            u_point[y] = x;
            u_parent[y] = false;
        } else {
            u_point[x] = y;
            u_parent[x] = false;

            if (u_rank[x] == u_rank[y]) {
                u_rank[y] = u_rank[y] + 1;
            }
        }

        u_disjoint -= 1;
    }
}

void ufds_gen_sizes() {
    free(u_sizes);
    u_sizes = calloc(u_size, sizeof(uint32_t));

    for (uint32_t i = 0; i < u_size; i++) {
        uint32_t p = ufds_find(i);
        u_sizes[p] += 1;
    }
    u_changed = false;
}

uint32_t ufds_size(uint32_t i) {
    if (u_sizes == NULL || u_changed) {
        ufds_gen_sizes();
    }

    return u_sizes[ufds_find(i)];
}

void ufds_free() {
    free(u_point);
    free(u_rank);

    u_disjoint = 0;
    u_size = 0;
    u_changed = false;
}

void test_ufds() {
    ufds_init(6);
    ufds_union(1, 3);
    assert(u_disjoint == 5);
    assert(ufds_is_same(1, 3));
    assert(!ufds_is_same(1, 2));
    assert(ufds_size(1) == 2);
    ufds_union(2, 4);
    assert(u_disjoint == 4);
    assert(ufds_is_same(1, 3));
    assert(!ufds_is_same(1, 2));
    assert(ufds_is_same(2, 4));
    assert(!ufds_is_same(1, 4));
    assert(ufds_size(2) == 2);
    ufds_union(2, 3);
    assert(u_disjoint == 3);
    assert(ufds_is_same(1, 3));
    assert(ufds_is_same(1, 2));
    assert(ufds_is_same(2, 4));
    assert(ufds_is_same(1, 4));
    assert(ufds_size(2) == 4);
    ufds_union(2, 1);
    assert(u_disjoint == 3);
    assert(ufds_is_same(1, 3));
    assert(ufds_is_same(1, 2));
    assert(ufds_is_same(2, 4));
    assert(ufds_is_same(1, 4));
    assert(ufds_size(2) == 4);
    ufds_free();
    //printf("PASSED UFDS TEST\n");
}

uint32_t s3i(uint32_t x, uint32_t y, uint32_t z) {
    uint32_t w = 1;
    return w*(5*y + x) + z;
}

uint64_t *theta(uint64_t *in_s) {
    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    uint32_t z = 0;

    uint64_t *c = calloc(5, sizeof(uint64_t));
    uint64_t *d = calloc(5, sizeof(uint64_t));
    for (uint32_t x = 0; x < 5; x++) {
        c[x] = in_s[s3i(x, 0, z)] ^ in_s[s3i(x, 1, z)] ^ in_s[s3i(x, 2, z)] ^ in_s[s3i(x, 3, z)] ^ in_s[s3i(x, 4, z)];
    }

    for (uint32_t x = 0; x < 5; x++) {
        d[x] = c[(x + 4) % 5] ^ c[(x+1)%5];
    }

    for (uint32_t x = 0; x < 5; x++) {
        for (uint32_t y = 0; y < 5; y++) {
            out_s[s3i(x, y, z)] = in_s[s3i(x, y, z)] ^ d[x];
        }
    }

    return out_s;
}

uint64_t *rho(uint64_t *in_s) {
    // Identity function for w=1

    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    for (uint32_t i = 0; i < 25; i++) {
        out_s[i] = in_s[i];
    }

    return out_s;
}

uint64_t *pi(uint64_t *in_s) {
    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    uint32_t z = 0;

    for (uint32_t x = 0; x < 5; x++) {
        for (uint32_t y = 0; y < 5; y++) {
            uint32_t nx = (x + 3*y) % 5;
            out_s[s3i(x, y, z)] = in_s[s3i(nx, x, z)];
        }
    }

    return out_s;
}

uint64_t *chi(uint64_t *in_s) {
    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    uint32_t z = 0;

    for (uint32_t x = 0; x < 5; x++) {
        for (uint32_t y = 0; y < 5; y++) {
            uint32_t nx1 = (x + 1) % 5;
            uint32_t nx2 = (x + 2) % 5;
            out_s[s3i(x, y, z)] = in_s[s3i(x, y, z)] ^ ((~in_s[s3i(nx1, y, z)]) & in_s[s3i(nx2, y, z)]);
        }
    }

    return out_s;
}

uint64_t iota_calc(uint32_t t) {
    uint16_t v = 1;
    if ((t % 255) == 0) {
        return 0xFFFFFFFFFFFFFFFFull;
    }

    for (uint64_t i = 1; i < (t % 255) + 1; i++) {
        v = v << 1;
        v = (v & 0b111111110) | ((v&1) ^ ((v >> 8) & 1));
        v = (v & 0b111101111) | ((((v >> 4) & 1) ^ ((v >> 8) & 1)) << 4);
        v = (v & 0b111011111) | ((((v >> 5) & 1) ^ ((v >> 8) & 1)) << 5);
        v = (v & 0b110111111) | ((((v >> 6) & 1) ^ ((v >> 8) & 1)) << 6);
        v = v & 0b11111111;
    }

    uint64_t ret = (uint64_t)(v & 1);
    for (uint64_t i = 0; i < 64; i++) {
        ret |= ret << 1;
    }

    return ret;
}

uint64_t *iota(uint64_t *in_s, uint32_t r) {
    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    uint32_t z = 0;

    for (uint32_t x = 0; x < 5; x++) {
        for (uint32_t y = 0; y < 5; y++) {
            out_s[s3i(x, y, z)] = in_s[s3i(x, y, z)];
        }
    }

    uint64_t iota_v = iota_calc(0 + 7*r);

    out_s[s3i(0, 0, 0)] = in_s[s3i(0, 0, 0)] ^ iota_v;

    return out_s;
}

uint64_t *to_state(uint32_t s) {
    uint64_t *ret = calloc(25, sizeof(uint64_t));
    for (uint64_t ns = 0; ns < 64; ns++) {
        uint64_t v = ns + (uint64_t)s;
        for (uint64_t o = 0; o < 25; o++) {
            ret[o] |= ((v >> (24ull - o)) & 1) << ns;
        }
    }
    return ret;
}

uint64_t *copy_state(uint64_t *in_s) {
    uint64_t *out_s = calloc(25, sizeof(uint64_t));
    uint32_t w = 1;
    for (uint32_t i = 0; i < 25; i++) {
        out_s[i] = in_s[i];
    }

    return out_s;
}

void print_state(uint64_t *in_s) {
    for (uint32_t x = 0; x < 5; x++) {
        for (uint32_t y = 0; y < 5; y++) {
            printf("%llu ", in_s[s3i(x, y, 0)]);
        }
        printf("\n");
    }
}

void update_ufds(uint32_t s, uint64_t *in_s) {
    for (uint64_t ns = 0; ns < 64; ns++) {
        uint64_t v = ns + (uint64_t)s;
        uint32_t ov = 0;
        for (uint32_t o = 0; o < 25; o++) {
            ov = ov << 1;
            ov |= (in_s[o] >> ns) & 1;
        }
        ufds_union(v, ov);
        if (v == ov) {
            printf("%u,", v, ov);
        }
    }
}

void test_iota() {
    assert(iota_calc(0) == 0xFFFFFFFFFFFFFFFFull);
    assert(iota_calc(7) == 0x0);
    assert(iota_calc(14) == 0x0);
    assert(iota_calc(21) == 0x0);
    assert(iota_calc(28) == 0xFFFFFFFFFFFFFFFFull);
}

int main(int argc, char** argv) {
    test_ufds();
    test_iota();
    uint32_t max = 1 << 25;
    uint32_t R = atoi(argv[1]);
    char *spec = argv[2];
    size_t spec_len = strlen(spec);

    ufds_init(max);

    printf("{\"fixed_points\": [");
    for (uint32_t s = 0; s < max; s += 64) {
        uint64_t *in_s = to_state(s);
        uint64_t *out_s = NULL;
        for (uint32_t r = 0; r < R; r++) {
            for (size_t s_p = 0; s_p < spec_len; s_p++) {
                char s_c = spec[s_p];
                if (s_c == 't') {
                    out_s = theta(in_s);
                    free(in_s);
                    in_s = copy_state(out_s);
                    free(out_s);
                } else if (s_c == 'r') {
                    out_s = rho(in_s);
                    free(in_s);
                    in_s = copy_state(out_s);
                    free(out_s);
                } else if (s_c == 'p') {
                    out_s = pi(in_s);
                    free(in_s);
                    in_s = copy_state(out_s);
                    free(out_s);
                } else if (s_c == 'c') {
                    out_s = chi(in_s);
                    free(in_s);
                    in_s = copy_state(out_s);
                    free(out_s);
                } else if (s_c == 'i') {
                    out_s = iota(in_s, r);
                    free(in_s);
                    in_s = copy_state(out_s);
                    free(out_s);
                }
            }
        }

        update_ufds(s, in_s);

        free(in_s);
    }
    printf("-1],\n");

    ufds_gen_sizes();

    printf("\"cycles\": %u,\n", u_disjoint);
    printf("\"cycle_map\": {");
    for (uint32_t s = 0; s < max; s++) {
        if (u_parent[s]) {
            printf("\"%u\": %u,", s, u_sizes[s]);
        }
    }
    printf("\"-1\": -1}}\n");

    ufds_free();
}
