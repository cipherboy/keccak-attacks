#include "stdio.h"
#include "sha3.h"
#include "stdint.h"

int test_iota_w8(void) {
    printf("Testing Keccak - iota: w8\n");
    size_t tests = 18;
    uint32_t args[18] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                          15, 16, 17 };
    inttype expected[18] = { 0x01, 0x82, 0x8A, 0x00, 0x8B, 0x01, 0x81, 0x09,
                             0x8A, 0x88, 0x09, 0x0A, 0x8B, 0x8B, 0x89, 0x03,
                             0x02, 0x80 };

    for (size_t i = 0; i < tests; i++) {
        inttype r = keccakrcinttype(args[i]);
        printf("\tTest [ %zu ] - Expected: %" PRIit " ; Got: %" PRIit "\n", i, expected[i], r);
        assert(r == expected[i]);
    }

    return 0;
}

int test_theta_w8(void) {
    printf("Testing Keccak - theta: w8\n");

    size_t tests = 2;
    inttype args[2][25] = { { 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }, { 0x83, 0x10, 0x80, 0x01, 0x90, 0x00, 0x00, 0x00, 0x20, 0x20, 0x02, 0x02, 0x00, 0x00, 0x00, 0x14, 0x00, 0x04, 0x10, 0x00, 0x01, 0x00, 0x05, 0x00, 0x04 } };
    inttype expected[2][25] = { { 0x01, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02 }, { 0x13, 0x87, 0xF0, 0xE9, 0x88, 0x90, 0x97, 0x70, 0xC8, 0x38, 0x92, 0x95, 0x70, 0xE8, 0x18, 0x84, 0x97, 0x74, 0xF8, 0x18, 0x91, 0x97, 0x75, 0xE8, 0x1C } };

    for (size_t i = 0; i < tests; i++) {
        State in = create_state(args[i]);
        State out = keccaktheta(in, 0);
        State exp = create_state(expected[i]);
        printf("\tTest [ %zu ]", i);
        for (size_t x = 0; x < 5; x++) {
            for (size_t y = 0; y < 5; y++) {
                if (out[x][y] != exp[x][y]) {
                    printf(" - FAIL\n");
                    print_state(out, "out");
                    print_state(exp, "expected");
                    assert(out[x][y] == exp[x][y]);
                }
            }
        }
        printf(" - PASS\n");
    }
    return 0;
}

int test_rho_w8(void) {
    printf("Testing Keccak - rho: w8\n");

    size_t tests = 2;
    inttype args[2][25] = { { 0x01, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02 }, { 0x13, 0x87, 0xF0, 0xE9, 0x88, 0x90, 0x97, 0x70, 0xC8, 0x38, 0x92, 0x95, 0x70, 0xE8, 0x18, 0x84, 0x97, 0x74, 0xF8, 0x18, 0x91, 0x97, 0x75, 0xE8, 0x1C } };
    inttype expected[2][25] = { { 0x01, 0x02, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x20, 0x00, 0x04, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x80 }, { 0x13, 0x0F, 0x3C, 0x9E, 0x44, 0x09, 0x79, 0x1C, 0x64, 0x83, 0x94, 0x56, 0x83, 0xD1, 0x0C, 0x09, 0xF2, 0x3A, 0x1F, 0x18, 0x46, 0x5E, 0xAE, 0xE8, 0x07 } };

    for (size_t i = 0; i < tests; i++) {
        State in = create_state(args[i]);
        State out = keccakrho(in, 0);
        State exp = create_state(expected[i]);
        printf("\tTest [ %zu ]", i);
        for (size_t x = 0; x < 5; x++) {
            for (size_t y = 0; y < 5; y++) {
                if (out[x][y] != exp[x][y]) {
                    printf(" - FAIL\n");
                    print_state(out, "out");
                    print_state(exp, "expected");
                    assert(out[x][y] == exp[x][y]);
                }
            }
        }
        printf(" - PASS\n");
    }
    return 0;
}

int test_pi_w8(void) {
    printf("Testing Keccak - pi: w8\n");

    size_t tests = 2;
    inttype args[2][25] = { { 0x01, 0x02, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x20, 0x00, 0x04, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x80 }, { 0x13, 0x0F, 0x3C, 0x9E, 0x44, 0x09, 0x79, 0x1C, 0x64, 0x83, 0x94, 0x56, 0x83, 0xD1, 0x0C, 0x09, 0xF2, 0x3A, 0x1F, 0x18, 0x46, 0x5E, 0xAE, 0xE8, 0x07 } };
    inttype expected[2][25] = { { 0x01, 0x10, 0x00, 0x00, 0x80, 0x00, 0x20, 0x00, 0x20, 0x00, 0x02, 0x00, 0x00, 0x02, 0x00, 0x10, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04 }, { 0x13, 0x79, 0x83, 0x1F, 0x07, 0x9E, 0x83, 0x94, 0xF2, 0xAE, 0x0F, 0x1C, 0xD1, 0x18, 0x46, 0x44, 0x09, 0x56, 0x3A, 0xE8, 0x3C, 0x64, 0x0C, 0x09, 0x5E } };

    for (size_t i = 0; i < tests; i++) {
        State in = create_state(args[i]);
        State out = keccakpi(in, 0);
        State exp = create_state(expected[i]);
        printf("\tTest [ %zu ]", i);
        for (size_t x = 0; x < 5; x++) {
            for (size_t y = 0; y < 5; y++) {
                if (out[x][y] != exp[x][y]) {
                    printf(" - FAIL out[%u][%u]\n", x, y);
                    print_state(out, "out");
                    print_state(exp, "expected");
                    assert(out[x][y] == exp[x][y]);
                }
            }
        }
        printf(" - PASS\n");
    }
    return 0;
}

int test_chi_w8(void) {
    printf("Testing Keccak - chi: w8\n");

    size_t tests = 2;
    inttype args[2][25] = { { 0x01, 0x10, 0x00, 0x00, 0x80, 0x00, 0x20, 0x00, 0x20, 0x00, 0x02, 0x00, 0x00, 0x02, 0x00, 0x10, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04 }, { 0x13, 0x79, 0x83, 0x1F, 0x07, 0x9E, 0x83, 0x94, 0xF2, 0xAE, 0x0F, 0x1C, 0xD1, 0x18, 0x46, 0x44, 0x09, 0x56, 0x3A, 0xE8, 0x3C, 0x64, 0x0C, 0x09, 0x5E } };
    inttype expected[2][25] = { { 0x01, 0x10, 0x80, 0x01, 0x90, 0x00, 0x00, 0x00, 0x20, 0x20, 0x02, 0x02, 0x00, 0x00, 0x00, 0x14, 0x00, 0x04, 0x10, 0x00, 0x01, 0x00, 0x05, 0x00, 0x04 }, { 0x91, 0x65, 0x83, 0x0F, 0x6F, 0x8A, 0xE1, 0x98, 0xE2, 0xAF, 0xCE, 0x14, 0x97, 0x11, 0x56, 0x12, 0x21, 0x96, 0x3E, 0xE1, 0x34, 0x65, 0x5A, 0x29, 0x1E } };

    for (size_t i = 0; i < tests; i++) {
        State in = create_state(args[i]);
        State out = keccakchi(in, 0);
        State exp = create_state(expected[i]);
        printf("\tTest [ %zu ]", i);
        for (size_t x = 0; x < 5; x++) {
            for (size_t y = 0; y < 5; y++) {
                if (out[x][y] != exp[x][y]) {
                    printf(" - FAIL out[%u][%u]\n", x, y);
                    print_state(out, "out");
                    print_state(exp, "expected");
                    assert(out[x][y] == exp[x][y]);
                }
            }
        }
        printf(" - PASS\n");
    }
    return 0;
}


int main() {
    test_theta_w8();
    test_rho_w8();
    test_pi_w8();
    test_chi_w8();
    test_iota_w8();
}
