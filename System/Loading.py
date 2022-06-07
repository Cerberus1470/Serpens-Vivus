import sys
import os
import time
import threading
import datetime


class Loading:
    def __init__(self, results, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.foo, args=results)
        thread.daemon = True
        thread.start()

    @staticmethod
    async def foo(results):
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


def returning(message, length=0):
    if length == 0:
        print(message, end='')
    for i in range(length):
        chars = '/—\\|'
        for char in chars:
            print('\r' + message + '\t' + char, end='')
            time.sleep(0.25)
            sys.stdout.flush()
    print()
    return


def returning_to_apps():
    returning("Returning to the Applications screen...", 2)


def progress_bar(message, length):
    for i in range(10):
        print('\r' + message + '\t[' + str('=' * i) + str('-' * (10 - i)) + ']', end='')
        time.sleep(length / 10.0)


def log(message=''):
    file = open("System\\event_log.info", 'a')
    file.write("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message + '\n')
    file.close()


def modify_user(username='', element=-1, value=''):
    if element < 0 or element > 14:
        return 0
    for subdir, dirs, files in os.walk("Users"):
        if subdir == "Users\\" + username:
            file = list(open("{}\\info.usr".format(subdir), 'r'))
            info = caesar_decrypt(file[0]).split('\t\t')
            programs = caesar_decrypt(file[1]).split('\n')[0].split('.')
            if element < 4:
                info[element] = value
            else:
                try:
                    programs[element-4] = value
                except IndexError:
                    break
            file = open("{}\\info.usr".format(subdir), 'w')
            file.write(caesar_encrypt('\t\t'.join(info)))
            file.write(caesar_encrypt('.'.join(programs) + '\n'))
            file.close()
            if element == 1:
                os.rename(subdir, "Users\\{}".format(value))
            return 1
    returning("An error occurred. Please reboot the system safely.", 2)
    return 0


def display_user(username=""):
    for subdir, dirs, files in os.walk("Users"):
        if subdir == "Users\\{}".format(username) and "info.usr" in files:
            file = list(open(subdir + "\\info.usr"))
            print(caesar_decrypt(file[0]))
            print(caesar_decrypt(file[1]))


def caesar_encrypt(message=''):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()`~-_=+[{]}|;:\'\",<.>/?\t'
    encrypted_h = ''
    key = [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]
    if len(key) <= len(message):
        key = key * int(len(message))
    for i in range(len(message)):
        if message[i] == '\n':
            encrypted_h += '\n'
        else:
            try:
                encrypted_h += alphabet[alphabet.index(message[i]) + key[i]]
            except IndexError:
                encrypted_h += alphabet[alphabet.index(message[i]) + key[i] - 95]
    return encrypted_h


def caesar_decrypt(encrypted_h=''):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()`~-_=+[{]}|;:\'\",<.>/?\t'
    decrypted_h = ''
    key = [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]
    if len(key) <= len(encrypted_h):
        key = key * int(len(encrypted_h))
    for i in range(len(encrypted_h)):
        if encrypted_h[i] == '\n':
            decrypted_h += '\n'
        else:
            try:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i]]
            except IndexError:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i] + 95]
    return decrypted_h


# noinspection PyTypeChecker
async def test():
    print("Hello world!")
    return 42