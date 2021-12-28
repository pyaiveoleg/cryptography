from sha_encrypt import sha_encrypt
from hashlib import sha1


def run():
    m = "I love cryptography!".encode("utf-8")
    print(f'digest: {sha_encrypt(m)}')
    print(f"library {sha1(m).hexdigest()}")


if __name__ == "__main__":
    run()
