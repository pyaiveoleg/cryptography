import logging

from aes.aes_tools import get_keys_i, add_round_key, print_table, columns_to_list, print_keys_i, multiply_matrices_in_galois
from aes.constants import s_box, multiplier_galois
from common.tools import list_cyclic_shift


def sub_bytes(state):
    return [s_box[byte] for byte in state]


def shift_rows(state):
    rows = [
        state[0:4],
        state[4:8],
        state[8:12],
        state[12:16],
    ]
    for i in range(4):
        rows[i] = list_cyclic_shift(i, rows[i])
    return rows[0] + rows[1] + rows[2] + rows[3]


def mix_columns(state):
    return multiply_matrices_in_galois(state, multiplier_galois)


def encrypt_aes(block, key):
    keys = get_keys_i(key)
    print_keys_i(keys)

    state = block
    logging.debug("before add_round_key")
    logging.debug(print_table(state))
    state = add_round_key(state, key)
    logging.debug("after add_round_key")
    logging.debug(print_table(state))

    n_r = 10
    n_b = 4
    for i in range(1, n_r):
        logging.debug(f"--------------ROUND {i}-----------------------")
        state = sub_bytes(state)
        logging.debug("after sub_bytes")
        logging.debug(print_table(state))
        state = shift_rows(state)
        logging.debug("after shift_rows")
        logging.debug(print_table(state))
        state = mix_columns(state)
        logging.debug("after mix_columns")
        logging.debug(print_table(state))
        state = add_round_key(state, columns_to_list(keys[i * n_b: (i + 1) * n_b]))
        logging.debug("after add_round_key")
        logging.debug(print_table(state))

    logging.debug(f"--------------ROUND 10-----------------------")
    state = sub_bytes(state)
    logging.debug("after sub_bytes")
    logging.debug(print_table(state))
    state = shift_rows(state)
    logging.debug("after shift_rows")
    logging.debug(print_table(state))
    state = add_round_key(state, columns_to_list(keys[n_r * n_b: (n_r + 1) * n_b]))
    logging.debug("after add_round_key")
    logging.debug(print_table(state))
    return state
