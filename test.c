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

int main() {
    test_iota_w8();
}
