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

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()`~-_=+[{]}|;:,<.>/?'


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


class HomeInterrupt(Exception):
    """
    Class HomeInterrupt. Houses the error to raise if the user wants to go home.
    """

    def __repr__(self):
        return "HomeInterrupt(Interrupt){}".format(self.args[0])
    # def __init__(self, app_object=None):
    #     self.app_object = app_object.get_saved_state() if app_object else None


class LockInterrupt(Exception):
    """
    Class LockInterrupt. Houses the error to raise if the user wants to lock the screen.
    """

    def __repr__(self):
        return "LockInterrupt(Interrupt){}".format(self.args[0])


def pocs_input(message, app_object=None):
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


def pass_input(prompt="Enter Password: ", mask="*", suppress=False):
    """
    CREDIT: Module maskpass.
    Description
    ----------
    An advanced version of the askpass which works in Spyder/Qtconsole and
    has a revealing feature

    Parameters
    ----------
    prompt : The prompt shown for asking password, optional
        DESCRIPTION. The default is "Enter Password: ".
    mask : The masking character, use "" for max security, optional
        DESCRIPTION. The default is "*".
    suppress : Pass True to stop QTConsole from jumping when Spacebar is pressed
        DESCRIPTION. Default is True
    Raises
    ------
    KeyboardInterrupt
        When CTRL+C pressed while typing the password

    Returns
    -------
    Password
        Returns the entered password as string type
        Returns empty string "" if Escape pressed

    """
    from pynput import keyboard

    print(prompt, end="", flush=True)

    to_reveal = False
    count = 0
    mask_length = len(mask)
    password_input = ""
    # try:
    #     # Checking if we're running in IPython/QtConsole/Spyder
    #     __IPYTHON__
    #     import IPython
    #     if(type(get_ipython())==IPython.terminal.interactiveshell.TerminalInteractiveShell):
    #         # Means its IPython but in terminal, so tty_check is set to True
    #         tty_check = True and not ide
    #     else:
    #         tty_check = False
    #
    # except NameError:
    #     tty_check = True and not ide
    shift_hold = False

    def on_press(key):
        """
        Method called when a key is pressed.
        :param key:
        :return:
        """
        nonlocal password_input, count, to_reveal, shift_hold

        try:
            if key.char in ["\x03"]:
                # CTRL+C character
                raise KeyboardInterrupt
            #
            # elif ctrl_hold and key.char.lower() == "c":
            #     # When using suppressed, CTRL+C doesn't get caught, so
            #     # this is a hacky way to detect that. Also raising error in
            #     # suppressed mode doesn't work, so it's raised later by
            #     # setting password_input as None
            #     password_input = None
            #     return False

            else:
                password_input += key.char.upper() if shift_hold else key.char.lower()
                # If to_reveal is True, it means the character which is
                # entered is printed, else, the masking character is printed
                char = key.char if to_reveal else mask
                print(char, end="", flush=True)
                if char != "":
                    count += 1

        except AttributeError:
            if key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
                # shift_hold stays true until released.
                shift_hold = True

            if key == keyboard.Key.enter:
                # End listening
                return False

            elif key == keyboard.Key.space:
                char = " " if to_reveal else mask
                print(char, end="", flush=True)
                password_input += " "
                count += 1

            elif key == keyboard.Key.backspace:
                password_input = password_input[:-1]
                # if count != 0:
                #     # In Spyder IDE, backspace character doesn't
                #     # work as expected for this, but a combination
                #     # of backspace and \u200c works. So
                #     # sys.stdout.isatty() is used to check whether
                #     # it's the IDE console or not.
                #     if tty_check:
                #         if to_reveal:
                #             print("\b \b", end="", flush=True)
                #         else:
                #             # Handling different length masking character
                #             print("\b \b"*mask_length, end="", flush=True)
                #     else:
                if to_reveal:
                    print("\b\u200c", end="", flush=True)
                else:
                    # Handling different length masking character
                    print(("\b"*mask_length)+("\u200c"*mask_length),
                          end="", flush=True)
                count -= 1

            elif key == keyboard.Key.ctrl_l:
                # Fancy way of revealing/unrevealing the characters
                # entered by pressing CTRL key
                to_reveal = not to_reveal

                if mask == "":
                    # If mask is "", then that means nothing has been
                    # printed while typing. So no need to remove characters
                    # from screen. Just straight up print the stuff
                    # typed before
                    if to_reveal:
                        print(password_input, end="", flush=True)
                        count = len(password_input)
                    else:
                        # Usual checking whether it's IDE/console
                        # if tty_check:
                        #     print("\b \b"*len(password_input),
                        #           end="", flush=True)
                        # else:
                        print(("\b"*len(password_input)) +
                              ("\u200c"*len(password_input)),
                              end="", flush=True)
                        count = 0
                else:
                    # If the mask isn't "", then something has been
                    # printed on the screen, and we need to remove it
                    # before printing the previously entered text
                    if to_reveal:
                        # The masking character could be multilength.
                        # So we print destructive backspace character
                        # times the length of previously entered
                        # text times the length of masking character
                        # to remove it completely
                        # if tty_check:
                        #     print(("\b \b"*len(password_input)*mask_length) +
                        #           password_input, end="", flush=True)
                        # else:
                        print(("\b"*len(password_input)*mask_length) +
                              ("\u200c"*len(password_input)*mask_length) +
                              password_input, end="", flush=True)
                    else:
                        # Just removing the printed text and printing
                        # the mask character to unreveal the text.
                        print(("\b"*len(password_input)) +
                              (mask*len(password_input)), end="", flush=True)

            elif key == keyboard.Key.esc:
                password_input = ""
                return False

            else:
                # We don't need anything else as input, so just-
                pass

    def on_release(key):
        """
        Function only for detecting CTRL key release
        """
        nonlocal shift_hold
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
            shift_hold = False

    # if tty_check:
    #     listener = keyboard.Listener(on_press=on_press)
    # else:
    # Passing suppress True prevents qtconsole from jumping on
    # pressing Spacebar
    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=suppress)

    listener.start()

    # if tty_check:
    #     # You see, if you're using advpass in normal console, it's
    #     # actually listening to the input in background, sort of like a
    #     # keylogger. So while you're focussing on the console and typing
    #     # into that, pynput is collecting input from the background,
    #     # at the same time the console is keeping the input in buffer waiting
    #     # to put text into the console. The problem here is that, after
    #     # using advpass, the entered text will get put into the console
    #     # when it allows input afterwards. So, if you call advpass first
    #     # and then input(), we will get the password_input return from
    #     # advpass, but the entered text will also get into the input()
    #     # But things work differently in Spyder. It doesn't keep it in
    #     # in buffer. So, to work in both the environments, we use a
    #     # dummy getch/posix_getch just to capture the input in console
    #     # which will run simultaneously with the background input
    #     # listening to remove it from buffer. It will stop
    #     # when Enter is pressed.
    #     cross_getch = CrossGetch()
    #     while True:
    #         dummy_key = cross_getch.getch()
    #         if dummy_key in [b"\r", b"\x1b"]:
    #             break
    #         elif dummy_key == b"\x03":
    #             print(flush=True)  # To put a newline before the error
    #             raise KeyboardInterrupt
    # else:
    try:
        listener.join()
    except KeyboardInterrupt as error:
        raise KeyboardInterrupt(error)

    print(flush=True)

    if password_input is None:
        raise KeyboardInterrupt

    return password_input


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
        if message[i] == '\n':
            encrypted_h += '\n'
        else:
            try:
                encrypted_h += alphabet[alphabet.index(message[i]) + key[i]]
            except IndexError:
                encrypted_h += alphabet[alphabet.index(message[i]) + key[i] - 92]
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
        if encrypted_h[i] == '\n':
            decrypted_h += '\n'
        else:
            try:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i]]
            except IndexError:
                decrypted_h += alphabet[alphabet.index(encrypted_h[i]) - key[i] + 92]
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


async def test():
    print("Hello world!")
    return 42
