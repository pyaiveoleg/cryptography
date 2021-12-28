from common.tools import decimal_to_binary, binary_to_decimal, fill_zeros
from sha.preprocessing import leftrotate, split_hex_number


def get_f_k(i: int, b, c, d):
    f, k = 0, 0  # guarantee to assign value
    if 0 <= i <= 19:
        f = (b & c) | ((~ b) & d)
        k = 0x5A827999
    elif 20 <= i <= 39:
        f = (b ^ c) ^ d
        k = 0x6ED9EBA1
    elif 40 <= i <= 59:
        f = (b & c) | (b & d) | (c & d)
        k = 0x8F1BBCDC
    elif 60 <= i <= 79:
        f = (b ^ c) ^ d
        k = 0xCA62C1D6
    return f, k


def sha_encrypt(message: bytes):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    parts = split_hex_number(int(message.hex(), 16), block_l=512)
    for part in parts:
        # разбиваем этот кусок на 16 частей, слов по 32-бита (big-endian) w[i], 0 <= i <= 15
        w = split_hex_number(part, block_l=32, add_blocks=False, add_trailing_zeros=512)
        for i in range(16, 80):  # 16 слов по 32-бита дополняются до 80 32-битовых слов
            w.append(leftrotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        for i in range(80):
            f, k = get_f_k(i, b, c, d)
            temp = (leftrotate(a, 5) + f + e + k + w[i]) % (2 ** 32)
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = temp
        h0 = (h0 + a) % (2 ** 32)
        h1 = (h1 + b) % (2 ** 32)
        h2 = (h2 + c) % (2 ** 32)
        h3 = (h3 + d) % (2 ** 32)
        h4 = (h4 + e) % (2 ** 32)
    digest = format(binary_to_decimal("".join(fill_zeros(decimal_to_binary(x), 32) for x in [h0, h1, h2, h3, h4])), "x")
    return digest
