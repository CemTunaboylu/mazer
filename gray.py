def gray_code_of(number: int) -> int:
    return number ^ (number >> 1)


# Each bit of original binary number may be recreated by
# taking the XOR of the corresponding bit in the gray_code
# with all the bits to its left (including the sign bit)
def from_gray_code(gray_code: int) -> int:
    number = gray_code  # the left-most bit
    while gray_code > 0:  # O(s) where s is the num. of set bits
        gray_code >> 1
        number ^= gray_code
    return number
