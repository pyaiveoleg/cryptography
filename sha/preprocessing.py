from common.tools import decimal_to_binary, apply_cyclic_shift, binary_to_decimal, fill_zeros


def add_symbols_to_last_block(binary: str):
    block_length = 512
    last_block: str = binary[len(binary) // block_length * block_length:]
    last_block_len = len(last_block)
    last_block_threshold = 448
    message_length = fill_zeros(decimal_to_binary(len(binary)), 64)  # big endian
    if last_block_len < last_block_threshold:
        return binary + "1" + "0" * (last_block_threshold - 1 - last_block_len) + message_length
    else:
        new_block = "0" * last_block_threshold + message_length
        return binary + "1" + "0" * (block_length - 1 - last_block_len) + new_block


def leftrotate(x: int, n: int):
    binary = fill_zeros(decimal_to_binary(x), 32)
    shifted = apply_cyclic_shift(n, binary)
    result = binary_to_decimal(shifted) % (2 ** 32)
    return result


def split_hex_number(m: int, block_l: int = 512, add_blocks=True, add_trailing_zeros=0):
    m_ = decimal_to_binary(m)
    if add_blocks:
        m_ = add_symbols_to_last_block(m_)
    m_ = fill_zeros(m_, add_trailing_zeros)
    if len(m_) % block_l != 0:
        raise Exception(f"Длина сообщения не делится на длину блока. len(m_) = {len(m_)}, block_l={block_l}")
    return [binary_to_decimal(m_[block_l * i:block_l * (i + 1)]) for i in range(len(m_) // block_l)]
