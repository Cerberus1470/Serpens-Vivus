"""
Module Loading. This module is similar to the Loading Program from the Matrix (name derived), and contains
many functions and classes that don't belong in any other file. A home for the homeless, if you will. It is
also used as a testing grounds.
"""
import os
import time

import random
import threading
import datetime
import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()`~-_=+[{]}|;:\'\",<.>/?\t'


class LoadingClass:
    """
    Class LoadingClass. This is a tester class for threaded processes.
    """
    def __init__(self, results, interval=1):
        self.results = results
        self.interval = interval
        self.interval2 = interval

    def thread(self):
        """
        This method starts a thread.
        :return: Nothing
        """
        thread = threading.Thread(target=self.foo)
        thread.daemon = True
        thread.start()
        time.sleep(6)
        if self.results > 5:
            print(self.results)

    def thread2(self):
        """
        This method creates a thread too.
        :return: Nothing
        """
        thread = threading.Thread(target=self.goo)
        thread.daemon = True
        thread.start()

    def goo(self):
        """
        This method is used for testing threads.
        :return: Nothing
        """
        while True:
            if self.interval != self.interval2:
                print(str(self.interval) + "! You changed it!")
                self.interval2 = self.interval

    def foo(self):
        """
        This method is used to increment a counter while a thread is running.
        :return:
        """
        for i in range(10):
            self.results += 1
            time.sleep(self.interval)


def animated_loading():
    """
    This is the first tester function, used to display a loading screen.
    :return:
    """
    chars = "/-\\|"
    for char in chars:
        print('\rloading...' + char, end='')
        time.sleep(0.26)
        sys.stdout.flush()


def returning(message, length=0):
    """
    This is the more polished version of the animated_loading function. Used everywhere to display a loading screen.
    :param message: The message to display alongside the loading ticker.
    :param length: How long the ticker should tick for, in seconds.
    :return: Nothing
    """
    if length == 0:
        print(message, end='')
    for i in range(length):
        for char in '/-\\|':
            print('\r' + message + '\t' + char, end='')
            time.sleep(0.25)
            sys.stdout.flush()
    print('\r' + message, end='')
    print()
    return


def returning_to_apps():
    """
    This is a parent method of returning() that offers an easier call to a widely-used loading message.
    :return: Nothing.
    """
    returning("Returning to the Applications screen...", 2)


def progress_bar(message, length):
    """
    This method displays a progress bar with a message. Similar to the returning() function, but shows a progress
    bar as opposed to a ticker.
    :param message: The message to display.
    :param length: How long the progress bar should run for, in seconds.
    :return: Nothing.
    """
    for i in range(1, 101):
        print('\r' + message + '\t[' + str('=' * int(i/10)) + str('-' * (9 - int(i/10))) + ']\t' + str(i) + '%', end='')
        time.sleep(length / 100.0)


def log(message=''):
    """
    This enters a log into the event_log.info file inside System.
    :param message: The message to log.
    :return: Nothing.
    """
    file = open("System\\event_log.info", 'a')
    file.write("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message + '\n')
    file.close()


def modify_user(username='', element=-1, value=''):
    """
    This method is used to permanently modify a user's info.usr file.
    :param username: The name of the user to modify.
    :param element: The element to change. Integer from 0-14.
    :param value: What value to set the element to.
    :return: 1 if successful, 0 if unsuccessful.
    """
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
                    programs[element - 4] = value
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
    """
    This is a tester method to display a user and all of its pertinent info.
    :param username: The name of the user to gather info about.
    :return: Nothing.
    """
    for subdir, dirs, files in os.walk("Users"):
        if subdir == "Users\\{}".format(username) and "info.usr" in files:
            file = list(open(subdir + "\\info.usr"))
            print(caesar_decrypt(file[0]))
            print(caesar_decrypt(file[1]))


def caesar_encrypt(message=''):
    """
    This is an advanced method to encrypt a string using a custom caesar cypher.
    :param message: The message to encrypt.
    :return: The encrypted message.
    """
    encrypted_h = ''
    message = str(message)
    key = [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]
    if len(key) <= len(message):
        key *= int(len(message))
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
    """
    This is the inverse of caesar_encrypt. This advanced method decrypts the message using the same custom
    caesar cypher.
    :param encrypted_h: The message to decrypt.
    :return: The decrypted message.
    """
    decrypted_h = ''
    key = [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]
    if len(key) <= len(encrypted_h):
        key *= int(len(encrypted_h))
    for i in range(len(encrypted_h)):
        if encrypted_h[i] == '\n':
            decrypted_h += '\n'
        else:
            try:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i]]
            except IndexError:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i] + 95]
    return decrypted_h


def caesar_encrypt_hex(message=''):
    """
    This is a custom advanced method using hexes to create encrypted text that is all the same length.
    :param message: Message to encrypt.
    :return: The encrypted hex message
    """
    encrypted_h = caesar_encrypt(message)
    if len(encrypted_h) < 100:
        return encrypted_h + '\\' + ''.join(random.choices(alphabet, k=99-len(encrypted_h)))
    elif len(encrypted_h) == 100:
        return encrypted_h
    else:
        encrypted_h = caesar_decrypt(encrypted_h)
        return caesar_encrypt(str(int(len(encrypted_h)/100)) + encrypted_h[0:int(100-int(len(encrypted_h)/100)/9)]) + '\n' + (caesar_encrypt_hex(encrypted_h[100-int(len(encrypted_h)/100):]))


buffer = []


def caesar_decrypt_hex(encrypted_h=''):
    """
    This is the inverse of caesar_encrypt_hex().
    :param encrypted_h: The encrypted message.
    :return: The decrypted message.
    """
    if '\\' in encrypted_h:
        return caesar_decrypt(encrypted_h.split('\\')[0])
    else:
        buffer.append(encrypted_h)
    if buffer:
        pass


# noinspection PyTypeChecker
async def test():
    print("Hello world!")
    return 42
