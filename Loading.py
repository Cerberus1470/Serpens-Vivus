import sys
import time
import threading
from cryptography.fernet import Fernet


class Loading:
    def __init__(self, results, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.foo, args=results)
        thread.daemon = True
        thread.start()

    @staticmethod
    def foo(results):
        while True:
            results += 1
            time.sleep(1)


# Here is an example of the process function:


def animated_loading():
    chars = "/—\\|"
    for char in chars:
        print('\rloading...' + char, end='')
        time.sleep(0.26)
        sys.stdout.flush()


def returning(message, length):
    for i in range(length):
        chars = '/—\\|'
        for char in chars:
            print('\r' + message + '\t' + char, end='')
            time.sleep(0.25)
            sys.stdout.flush()


def caesar_cypher():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    h = "hzxlo"
    encrypted_h = ''
    decrypted_h = ''
    print(h)
    key = [0, 4, 3, 5, 7, 8, 1, 2, 9, 6]
    if len(key) <= len(h):
        key = key * (len(h) / 10.0)
    for i in range(len(h)):
        try:
            encrypted_h += alphabet[alphabet.index(h[i]) + key[i]]
        except IndexError:
            encrypted_h += alphabet[alphabet.index(h[i]) + key[i] - 26]
    print(encrypted_h)
    for i in range(len(encrypted_h)):
        try:
            decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i]]
        except IndexError:
            decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i] + 26]
    print(decrypted_h)


def testing_hash():
    # we will be encrypting the below string.
    message = "hello geeks"

    # generate a key for encryption and decryption
    # You can use fernet to generate
    # the key or use random key generator
    # here I'm using fernet to generate key

    key = Fernet.generate_key()
    # Instance the Fernet class with the key

    fernet = Fernet(key)

    # then use the Fernet class instance
    # to encrypt the string string must must
    # be encoded to byte string before encryption
    encMessage = fernet.encrypt(message.encode())

    print("original string: ", message)
    print("encrypted string: ", encMessage)

    # decrypt the encrypted string with the
    # Fernet instance of the key,
    # that was used for encrypting the string
    # encoded byte string is returned by decrypt method,
    # so decode it to string with decode methods
    decMessage = fernet.decrypt(encMessage).decode()

    print("decrypted string: ", decMessage)

    print(key)
