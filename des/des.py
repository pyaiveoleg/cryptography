import logging
import sys

from constants import *
from common.tools import *


def apply_feistel(block: str, key_i: str, i: int, reverse=False):
    left = block[:32]
    right = block[32:]
    l_next = right
    if reverse:
        r_next = xor(right, feistel_function(left, key_i, i))
    else:
        r_next = xor(left, feistel_function(right, key_i, i))
    logging.debug(f"l_{i} = {l_next}, r_{i} = {r_next}")
    res = l_next + r_next
    logging.debug(f"result: {res}")
    return res


def extend_block(block: str):
    if len(block) != 32:
        raise Exception("Incorrect block length for Feistel function.")
    res = ""
    for number in extension_table:
        res += block[number - 1]  # index from 0
    return res


def feistel_function(block: str, key_i: str, i: int):
    res = extend_block(block)
    logging.debug(f"E(R_{i - 1}): {res}")
    res = xor(res, key_i)
    logging.debug(f"Block after xor: {res}")
    resulting_b = ""
    for index, block_b in enumerate(grouper(res, 6)):  # 8 blocks with 6 bits
        a = binary_to_decimal(block_b[0] + block_b[-1])  # first and last
        b = binary_to_decimal(block_b[1:-1])  # all except first and last
        logging.debug(f"a: {a}, b: {b}")
        result = fill_zeros(decimal_to_binary(blocks_transform_table[index][a][b]), 4)
        resulting_b += result
    logging.debug(f"Resulting B_i: {resulting_b}")
    res = apply_permutation(final_feistel_permutation_table, resulting_b)
    logging.debug(f"result feistel function: {res}")
    return res


def get_additional_bits(key):
    res = ""
    for chunk in grouper(key, 7):
        li = list(chunk)
        res += "".join(li)
        ones_count = 0
        for char in li:
            if char == "1":
                ones_count += 1

        if ones_count % 2 == 0:
            res += "1"
        else:
            res += "0"
    return res


def get_keys_i(key):
    res = [""]
    logging.debug(f"Key: {key}")
    key = get_additional_bits(key)
    logging.debug(f"Key with additional bits: {key}")
    key = apply_permutation(key_start_permutation_table, key)
    logging.debug(f"Permuted key: {key}")
    c = key[:28]
    d = key[28:]
    logging.debug(f"c_0: {c}")
    logging.debug(f"d_0: {d}")

    for i in range(1, 17):
        c = apply_cyclic_shift(cyclic_shifts[i - 1], c)
        d = apply_cyclic_shift(cyclic_shifts[i - 1], d)
        logging.debug(f"c_{i}: {c}")
        logging.debug(f"d_{i}: {d}")
        key_i = apply_permutation(key_end_permutation_table, c + d)
        logging.debug(f"k_{i}: {key_i}")
        res.append(key_i)
    return res


def encrypt_des(block, key):
    block = apply_permutation(IP_permutation_table, block)
    logging.debug(f"Permuted text: {block}")
    keys = get_keys_i(key)
    for i in range(1, 17):
        logging.debug("Feistel start")
        block = apply_feistel(block, keys[i], i)
        logging.debug("Feistel end")
        logging.debug(block)
    right = block[32:]
    left = block[:32]
    block = apply_permutation(IP_reverse_permutation_table, right + left)
    return block


def decrypt_des(block, key):
    block = apply_permutation(IP_permutation_table, block)
    logging.debug(f"Permuted text: {block}")
    keys = get_keys_i(key)
    for i in range(16, 0, -1):
        block = apply_feistel(block, keys[i], i)
        logging.debug("Feistel end")
        logging.debug(block)
    right = block[32:]
    left = block[:32]
    block = apply_permutation(IP_reverse_permutation_table, right + left)
    return block


def run():
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    key = "0001001 0011010 0101011 0111100 1001101 1011110 1101111 1111000"
    text = "0000000100100011010001010110011110001001101010111100110111101111"

    key = key.replace(" ", "")
    cryptotext = encrypt_des(text, key)

    print(f"M = {text}")
    print(f"c = {cryptotext}")
    print(f"Decrypted c = {decrypt_des(cryptotext, key)}")


if __name__ == "__main__":
    run()
