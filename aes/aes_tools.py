import logging

from constants import *
from common.tools import *


def sub_bytes(state):
    return [s_box[byte] for byte in state]


def add_round_key(state, key_i):
    return [a ^ b for a, b in zip(state, key_i)]  # ^ is XOR


def get_keys_i(key):
    key_columns = get_columns(key)
    res_columns = [x for x in key_columns]

    current_index = 4
    for i in range(1, 11):
        first_column = [
            a ^ b ^ c for a, b, c in zip(
                res_columns[current_index - 4],
                sub_bytes(list_cyclic_shift(1, res_columns[current_index - 1])),
                r_con[i]
            )
        ]
        res_columns.append(first_column)
        current_index += 1
        for j in range(3):
            res_columns.append([a ^ b for a, b in zip(res_columns[current_index - 4], res_columns[current_index - 1])])
            current_index += 1
    return res_columns


def print_keys_i(keys_i):
    logging.debug(keys_i)
    for i in range(1, 10 + 1):
        logging.debug(f"key {i}")
        logging.debug(print_table(columns_to_list(keys_i[i * 4: (i + 1) * 4])))


def print_table(table: list):
    return "".join(f"\n{list(map(hex, group))}" for group in grouper(table, 4))


def columns_to_list(columns):
    return [column[0] for column in columns] + \
           [column[1] for column in columns] + \
           [column[2] for column in columns] + \
           [column[3] for column in columns]


def rows_to_list(rows):
    return [x for row in rows for x in row]


def get_columns(state):
    return [
        [state[0], state[4], state[8], state[12]],
        [state[1], state[5], state[9], state[13]],
        [state[2], state[6], state[10], state[14]],
        [state[3], state[7], state[11], state[15]]
    ]


def get_rows(state):
    return [
        state[0:4],
        state[4:8],
        state[8:12],
        state[12:16],
    ]


def multiply_matrices_in_galois(state, matrix):
    res_columns = []
    columns = get_columns(state)
    for column in columns:
        res_column = []
        for i in range(len(column)):
            elem = 0
            for j in range(len(column)):
                mul = matrix[4 * i + j]
                if mul == 1:
                    elem = elem ^ column[j]
                else:
                    elem = elem ^ multiply_by[mul][column[j]]
            res_column.append(elem)
        res_columns.append(res_column)
    return columns_to_list(res_columns)
