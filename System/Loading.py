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
import itertools

# MARKER: GLOBAL VARIABLES
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()`~-_=+[{]}|;:,<.>/?'

ATTRIBUTES = {
    "bold": 1,
    "dark": 2,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
}

HIGHLIGHTS = {
    "on_black": 40,
    "on_grey": 40,  # Actually black but kept for backwards compatibility
    "on_red": 41,
    "on_green": 42,
    "on_yellow": 43,
    "on_blue": 44,
    "on_magenta": 45,
    "on_cyan": 46,
    "on_light_grey": 47,
    "on_dark_grey": 100,
    "on_light_red": 101,
    "on_light_green": 102,
    "on_light_yellow": 103,
    "on_light_blue": 104,
    "on_light_magenta": 105,
    "on_light_cyan": 106,
    "on_white": 107
}

COLORS = {
    "black": 30,
    "grey": 30,  # Actually black but kept for backwards compatibility
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "light_grey": 37,
    "dark_grey": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_magenta": 95,
    "light_cyan": 96,
    "white": 97,
    "default": 0
}

BACKGROUNDS = set([k for k in itertools.chain.from_iterable([j for j in [[i for i in files if i.rpartition('.')[2] == "bg"] for subdir, dirs, files in os.walk("System")] if j] +
                                                            [j for j in [[i for i in files if i.rpartition('.')[2] == "bg"] for subdir, dirs, files in os.walk("Users")] if j])])

SPEED = 1.0


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


# MARKER: INTERRUPTS
class HomeInterrupt(Exception):
    """
    Class HomeInterrupt. Houses the error to raise if the user wants to go home.
    """

    def __repr__(self):
        return "HomeInterrupt(Interrupt){}".format(self.args[0].__getstate__())


class LockInterrupt(Exception):
    """
    Class LockInterrupt. Houses the error to raise if the user wants to lock the screen.
    """

    def __repr__(self):
        return "LockInterrupt(Interrupt){}".format(self.args[0].__getstate__())


# MARKER: CUSTOM PRINT/INPUT
def colored(message="", color=0):
    """
    This method returns colored text.
    :param message: The message to print
    :param color: What color to print it in. Can be a name or integer value.
    :return: The colored text, None if color is unrecognized.
    """
    if color in list(COLORS.keys()):
        return "\033[{color}m{msg}".format(color=(COLORS[color]), msg=message)
    elif color in list(COLORS.values()):
        return "\033[{color}m{msg}".format(color=color, msg=message)
    return None


def pocs_input(message="", app_object=None):
    """
    This method collects an input and checks for universal commands.
    :param message: Input message to use. The same as putting a message in an input statement.
    :param app_object: Object to pass back to store in the current user's saved_state. Leave blank to store no object.
    :return: The HomeInterrupt Object if the user typed "_home", and the input collection otherwise.
    """
    temp = input(message)
    if temp == "_home":
        raise HomeInterrupt(app_object)
    elif temp == "_lock":
        raise LockInterrupt(app_object)
    else:
        return temp


def pass_input(prompt="Enter Password: ", mask="*"):
    """
    Credit: module Maskpass. Modified to work with Python 3.12 and for the purposes of this project.
    An advanced version of the askpass which has a revealing feature.
    :param prompt: The prompt shown for asking password, optional. The default is "Enter Password: ".
    :param mask: The masking character, use "" for max security, optional. The default is "*".
    :return: Entered password as a string, or empty string if esc pressed.
    :raises: KeyboardInterrupt when CTRL+C pressed while typing the password.
    """
    from pynput import keyboard
    print(prompt, end="", flush=True)
    to_reveal = False  # Reveal characters?
    password_input = ""  # The actual input.
    shift_hold = False  # When using suppressed, capital letters don't get caught, so this is a hacky way to detect that.

    def on_press(key):
        """
        Method to handle keypresses.
        :param key: The key pressed, of type pynput.Keyboard.Key.
        :return: False to stop the listener.
        """
        nonlocal password_input, to_reveal, shift_hold

        try:
            if key.char in ["\x03"]:  # CTRL+C character
                raise KeyboardInterrupt
            else:
                password_input += key.char.upper() if shift_hold else key.char.lower()  # If to_reveal is True, it means the character which is entered is printed, else, the masking character is printed.
                print((key.char.upper() if shift_hold else key.char.lower()) if to_reveal else mask, end="", flush=True)
        except AttributeError:
            if key in [keyboard.Key.shift_r, keyboard.Key.shift_l]:
                shift_hold = True  # shift_hold stays True until it's released
            if key == keyboard.Key.enter:
                return False  # End listening
            elif key == keyboard.Key.space:
                password_input += " "
                print(" " if to_reveal else mask, end="", flush=True)

            elif key == keyboard.Key.backspace:
                if mask != "" and len(password_input) != 0:
                    password_input = password_input[:-1]
                    print(("\b \b" * (1 if to_reveal else len(mask))), end="", flush=True)  # \b only moves the cursor back, so we go back, print a space, then go back again.

            elif key == keyboard.Key.ctrl_l:  # Fancy way of revealing/unrevealing the characters entered by pressing CTRL key
                to_reveal = not to_reveal
                if mask == "":  # Nothing has been printed while typing. So just straight up print the stuff typed before.
                    print(password_input if to_reveal else ("\b \b" * len(password_input)), end="", flush=True)
                else:  # Something has been printed on the screen, and we need to remove it before printing the previously entered text.
                    print("{backspace}{after}".format(
                        backspace="\b \b" * len(password_input) * (len(mask) if to_reveal else 1),
                        after=password_input if to_reveal else mask * len(password_input)
                    ), end="", flush=True)
            elif key == keyboard.Key.esc:  # Debug way to get out!
                password_input = ""
                return False

    def on_release(key):
        """
        Function only for detecting SHIFT key release
        """
        nonlocal shift_hold
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
            shift_hold = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)  # Initialize listener.
    listener.start()
    try:
        listener.join()
    except KeyboardInterrupt as error:
        raise KeyboardInterrupt(error)
    print(flush=True)
    if password_input is None:
        raise KeyboardInterrupt
    return password_input


# MARKER: Animations
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


def returning(message="", length=0):
    """
    This is the more polished version of the animated_loading function. Used everywhere to display a loading screen.
    :param message: The message to display alongside the loading ticker.
    :param length: How long the ticker should tick for, in seconds.
    :return: Nothing
    """
    if '\n' in message:  # Code to print out multi-line returning.
        print(message.rpartition('\n')[0])
        message = message.rpartition('\n')[2]
    if length == 0:
        print(message, end='')
    for i in range(length):
        for char in '/-\\|':
            print('\r' + message + '\t' + char, end='')
            time.sleep(0.25 / SPEED)
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
        print('\r' + message + '\t[' + str('=' * int(i / 10)) + str('-' * (9 - int(i / 10))) + ']\t' + str(i) + '%', end='')
        time.sleep(length / 100.0 / SPEED)


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
    :param element: The element to change. Integer from 0-3.
    :param value: What value to set the element to.
    :return: 0 if successful, 1 if unsuccessful.
    """
    if element < 0 or element > 3:
        return 0
    for subdir, dirs, files in os.walk("Users"):
        if subdir == "Users\\" + username:
            file = list(open("{}\\info.usr".format(subdir), 'r'))
            info = caesar_decrypt(file[0]).split('(U)')
            # programs = caesar_decrypt(file[1]).split('\n')[0].split('(P)')
            if element < 4:
                info[element] = value
            # else:
            #     try:
            #         programs[element - 4] = value
            #     except IndexError:
            #         break
            file = open("{}\\info.usr".format(subdir), 'w')
            file.write(caesar_encrypt('(U)'.join(info)))
            # file.write(caesar_encrypt('(P)'.join(programs) + '\n'))
            file.close()
            if element == 1:
                os.rename(subdir, "Users\\{}".format(value))
            return 0
    returning("An error occurred. Please reboot the system safely.", 2)
    return 1


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


def upscale(file, resolution):
    """
    This is a tester method to upscale wallpapers. It doesn't work quite as well as manual. But it does help.
    :param file:
    :param resolution:
    :return:
    """
    image = [i.replace("\n", "") for i in list(open(file, 'r'))] if file.__class__ == str else file
    upscaled_image = [[' ' for _ in range(40 * resolution)] for _ in range(10 * resolution)]
    for i in range(len(image)):
        for j in range(len(image[i])):
            match image[i][j]:
                case '_':
                    char = [[' ', ' '], ['_', '_']]
                case '/':
                    char = [[' ', '/'], ['/', ' ']]
                case '\\':
                    char = [['\\', ' '], [' ', '\\']]
                case _:
                    char = [[' ', ' '], [' ', ' ']]
            for k in range(i*2, i*2+2):
                for l in range(j*2, j*2+2):
                    upscaled_image[k][l] = char[k-i*2][l-j*2]
    return upscaled_image


def caesar_encrypt(message='', priority=1):
    """
    This is an advanced method to encrypt a string using a custom caesar cypher.
    :param message: The message to encrypt.
    :param priority: The priority with which to encrypt. This modifies the key to use so that different elements use a
    different encryption algorithm.
    :return: The encrypted message.
    """
    encrypted_h = ''
    message = str(message)
    key = [i * priority for i in [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]]
    if len(key) <= len(message):
        key *= int(len(message))
    for i in range(len(message)):
        if message[i] not in ALPHABET:
            encrypted_h += message[i]
        else:
            try:
                encrypted_h += ALPHABET[ALPHABET.index(message[i]) + key[i]]
            except IndexError:
                encrypted_h += ALPHABET[ALPHABET.index(message[i]) + key[i] - 92]
    return encrypted_h


def caesar_decrypt(encrypted_h='', priority=1):
    """
    This is the inverse of caesar_encrypt. This advanced method decrypts the message using the same custom
    caesar cypher.
    :param encrypted_h: The message to decrypt.
    :param priority: The priority with which to encrypt. This modifies the key to use so that different elements use a
    different encryption algorithm.
    :return: The decrypted message.
    """
    decrypted_h = ''
    key = [i * priority for i in [10, 4, 3, 5, 7, 8, 1, 2, 9, 6]]
    if len(key) <= len(encrypted_h):
        key *= int(len(encrypted_h))
    for i in range(len(encrypted_h)):
        if encrypted_h[i] not in ALPHABET:
            decrypted_h += encrypted_h[i]
        else:
            try:
                decrypted_h += ALPHABET[ALPHABET.index(encrypted_h[i]) - key[i]]
            except IndexError:
                decrypted_h += ALPHABET[ALPHABET.index(encrypted_h[i]) - key[i] + 92]
            except ValueError:
                return encrypted_h[i]
    return decrypted_h


def caesar_encrypt_hex(message=''):
    """
    This is a custom advanced method using hexes to create encrypted text that is all the same length.
    :param message: Message to encrypt.
    :return: The encrypted hex message
    """
    encrypted_h = caesar_encrypt(message)
    if len(encrypted_h) < 98:
        space = random.randint(10, 20)
        return caesar_encrypt("{space}{msg}{stuff}".format(
            space=space, msg=encrypted_h, stuff=''.join(random.choices(ALPHABET, k=98 - space - len(encrypted_h)))))
    elif len(encrypted_h) == 100:
        return encrypted_h
    else:
        encrypted_h = caesar_decrypt(encrypted_h)
        return caesar_encrypt(str(int(len(encrypted_h) / 100)) + encrypted_h[0:int(100 - int(len(encrypted_h) / 100) / 9)]) + '\n' + (caesar_encrypt_hex(encrypted_h[100 - int(len(encrypted_h) / 100):]))


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


async def test():
    print("Hello world!")
    return 42
