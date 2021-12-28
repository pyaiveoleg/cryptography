import math
import random


def euclidean_algorithm(a: int, b: int):
    while a % b != 0:
        r = a % b
        a = b
        b = r
    return b


def get_nod_linear_representation(a_i, b_i, q_i, r_i):
    coeffs = (1, -q_i[-1])
    for i in range(len(q_i) - 2, 0, -1):
        a, b = coeffs
        coeffs = (b, a - b * q_i[i])
    return coeffs


def get_modulo_reverse_deduction(x: int, module: int):
    if euclidean_algorithm(x, module) != 1:
        raise Exception("Число X не взаимно просто с модулем, обратного вычета не существует.")

    index = 0 if x > module else 1

    a = min(module, x)
    b = max(module, x)
    a_i = []
    b_i = []
    q_i = []
    r_i = []
    while a % b != 0:
        a_i.append(a)
        b_i.append(b)
        r = a % b
        r_i.append(r)
        q_i.append(a // b)
        a = b
        b = r
    coeffs = get_nod_linear_representation(a_i, b_i, q_i, r_i)
    return coeffs[index] % module   # can be negative, to fit


def decrypt_rsa(m: int, e: int, n: int):
    res = (m ** e) % n
    return res


def encrypt_rsa(m: int, d: int, n: int):
    res = (m ** d) % n
    return res


def get_random_number_mutually_simple_with(fi_n):
    e_found = False
    e = 0
    while not e_found:
        e = random.randint(1, fi_n)
        if euclidean_algorithm(e, fi_n) == 1:
            e_found = True
    return e


def get_random_primary_number(max_n):
    e_found = False
    e = 0
    while not e_found:
        e = random.randint(1, max_n)
        if check_primary(e):
            e_found = True
    return e


def check_primary(n):
    if n == 1:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def run():
    max_num = 100
    p = 71
    q = 83
    p = get_random_primary_number(max_num)
    q = get_random_primary_number(max_num)
    print(p, q)

    fi_n = (p - 1) * (q - 1)
    n = p * q

    m = get_random_number_mutually_simple_with(n)
    e = get_random_number_mutually_simple_with(fi_n)
    print(f"fi (n): {fi_n}")
    print(f"Шифрующая экспонента (е): {e}")
    d = get_modulo_reverse_deduction(e, fi_n)
    print(f"Дешифрующая экспонента (d): {d}")

    encrypted_message = encrypt_rsa(m, e, n)
    decrypted_message = decrypt_rsa(encrypted_message, d, n)
    print(f"Исходное сообщение: {m}")
    print(f"Зашифрованное сообщение: {encrypted_message}")
    print(f"Расшифрованное сообщение: {decrypted_message}")


if __name__ == "__main__":
    run()
