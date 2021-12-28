from aes_tools import get_keys_i, add_round_key, columns_to_list, multiply_matrices_in_galois
from constants import inv_s_box, inv_multiplier_galois
from common.tools import inv_list_cyclic_shift


def inv_sub_bytes(state):
    return [inv_s_box[byte] for byte in state]


def inv_shift_rows(state):
    rows = [
        state[0:4],
        state[4:8],
        state[8:12],
        state[12:16],
    ]
    for i in range(4):
        rows[i] = inv_list_cyclic_shift(i, rows[i])
    return rows[0] + rows[1] + rows[2] + rows[3]


def inv_mix_columns(state):
    return multiply_matrices_in_galois(state, inv_multiplier_galois)


def decrypt_aes(block, key):
    keys = get_keys_i(key)
    n_r = 10
    n_b = 4
    state = block
    state = add_round_key(state, columns_to_list(keys[n_r * n_b: (n_r + 1) * n_b]))

    for i in range(n_r - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, columns_to_list(keys[i * n_b: (i + 1) * n_b]))
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, key)

    return state
