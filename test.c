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

    size_t tests = 1;
    inttype args[1][25] = { { 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 } };
    inttype expected[1][25] = { { 0x01, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02 } };

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

    size_t tests = 1;
    inttype args[1][25] = { { 0x01, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x02 } };
    inttype expected[1][25] = { { 0x01, 0x02, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x20, 0x00, 0x04, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x80 } };

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

    size_t tests = 1;
    inttype args[1][25] = { { 0x01, 0x02, 0x00, 0x00, 0x10, 0x00, 0x10, 0x00, 0x00, 0x20, 0x00, 0x04, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x80 } };
    inttype expected[1][25] = { { 0x01, 0x10, 0x00, 0x00, 0x80, 0x00, 0x20, 0x00, 0x20, 0x00, 0x02, 0x00, 0x00, 0x02, 0x00, 0x10, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04 } };

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

    size_t tests = 1;
    inttype args[1][25] = { { 0x01, 0x10, 0x00, 0x00, 0x80, 0x00, 0x20, 0x00, 0x20, 0x00, 0x02, 0x00, 0x00, 0x02, 0x00, 0x10, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04 } };
    inttype expected[1][25] = { { 0x01, 0x10, 0x80, 0x01, 0x90, 0x00, 0x00, 0x00, 0x20, 0x20, 0x02, 0x02, 0x00, 0x00, 0x00, 0x14, 0x00, 0x04, 0x10, 0x00, 0x01, 0x00, 0x05, 0x00, 0x04 } };

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
