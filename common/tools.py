from itertools import zip_longest


def xor(str_1, str_2):
    def xor_elem(elem_1, elem_2):
        if elem_1 not in ["0", "1"] or elem_2 not in ["0", "1"]:
            raise Exception("Incorrect string for xor")
        if elem_1 == elem_2:
            return "0"
        else:
            return "1"
    return "".join(xor_elem(x, y) for x, y in zip(str_1, str_2))


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def apply_permutation(permutation_table: list, block: str):
    res = ""
    for number in permutation_table:
        res += block[number - 1]  # index from 0
    return res


def apply_cyclic_shift(n: int, block):
    for i in range(n):
        block = block[1:] + block[0]
    return block


def list_cyclic_shift(n: int, block):
    for i in range(n):
        block = block[1:] + [block[0]]
    return block


def inv_list_cyclic_shift(n: int, block):
    for i in range(n):
        block = [block[-1]] + block[:-1]
    return block


def binary_to_decimal(binary: str):
    res = 0
    n = len(binary) - 1
    for index, symbol in enumerate(binary):
        res += int(symbol) * (2 ** (n - index))
    return res  # % (2 ** 32)


def decimal_to_binary(decimal: int, add_trailing_zeros=True):
    r = bin(decimal)[2:]
    if add_trailing_zeros:
        k = len(r) if len(r) % 8 == 0 else(int(len(r) / 8) + 1) * 8
        r = fill_zeros(r, k)
    return r


def fill_zeros(binary: str, length: int):
    return "0" * (length - len(binary)) + binary
