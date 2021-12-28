import logging
import sys

from aes.aes_tools import get_columns, rows_to_list
from decrypt_aes import decrypt_aes
from encrypt_aes import encrypt_aes


def hex_print(table):
    return list(map(hex, rows_to_list(get_columns(table))))


def run():
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # That s my Kung Fu (16 ASCII characters, 1 byte each)
    key = [
        0x54, 0x73, 0x20, 0x67,
        0x68, 0x20, 0x4b, 0x20,
        0x61, 0x6d, 0x75, 0x46,
        0x74, 0x79, 0x6e, 0x75
    ]

    # Two One Nine Two (16 ASCII characters, 1 byte each)
    text = [
        0x54, 0x4F, 0x4E, 0x20,
        0x77, 0x6E, 0x69, 0x54,
        0x6F, 0x65, 0x6E, 0x77,
        0x20, 0x20, 0x65, 0x6F
    ]

    cryptotext = encrypt_aes(text, key)
    print(f"M = {hex_print(text)}")
    print(f"c = {hex_print(cryptotext)}")
    print(f"Decrypted c = {hex_print(decrypt_aes(cryptotext, key))}")


if __name__ == "__main__":
    run()
