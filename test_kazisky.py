import math


def char_to_number(char):
    return ord(char.lower()) - 97


def number_to_char(number):
    return chr(number + 97)


def vizhner_encrypt(text, key="mouse"):
    key_len = len(key)
    result = ""
    for i, symbol in enumerate(text):
        is_not_letter = ord(symbol) <= 96 or ord(symbol) >= 123
        if is_not_letter:
            continue
        symbol_code = char_to_number(symbol)
        key_code = char_to_number(key[i % key_len])
        result += number_to_char((symbol_code + key_code) % 26)
    return result


def get_divisors(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                large_divisors.append(int(n / i))
    for divisor in reversed(large_divisors):
        yield divisor


def distances(numbers: list):
    res = []
    for first_index in range(len(numbers)):
        for second_index in range(first_index):
            res.append(numbers[first_index] - numbers[second_index])
    return res


def run_kazisky_test(text):
    res = 0
    bigrams = {}  # ab -> list index of a
    for index in range(len(text) - 1):
        bigram = text[index] + text[index + 1]
        if bigram not in bigrams:
            bigrams[bigram] = []
        bigrams[bigram].append(index)
    import json
    print(json.dumps(bigrams, indent=4))
    divisors_frequency = {}
    distances_frequency = {}

    # for key, value in filter(lambda x: len(x[1]) > 5, bigrams.items()):
    for key, value in bigrams.items():
        for dist in distances(bigrams[key]):
            if dist not in distances_frequency:
                distances_frequency[dist] = 0
            distances_frequency[dist] += 1
            for divisor in get_divisors(dist):
                if divisor not in divisors_frequency:
                    divisors_frequency[divisor] = 0
                divisors_frequency[divisor] += 1
    # print(json.dumps(divisors_frequency, indent=4))
    # print(sorted(distances_frequency.items(), key=lambda k: k[0]))
    print(sorted(divisors_frequency.items(), key=lambda k: k[0]))
    # print(sorted(bigrams.items(), key=lambda k: -len(k[1])))
    return res


if __name__ == "__main__":
    with open("text.txt", "r", encoding="utf-8") as fin:
        t = fin.read().lower()
        # t = "abcabcabcaabcabcabca"
        encrypted_text = vizhner_encrypt(t, key="superkeyit")
        print(t)
    print(encrypted_text)
    run_kazisky_test(encrypted_text)
