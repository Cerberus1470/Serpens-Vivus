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

BACKGROUNDS = [k for k in itertools.chain.from_iterable([j for j in [[i for i in files if i.split('.')[1] == "bg"] for subdir, dirs, files in os.walk("System")] if j] +
                                                        [j for j in [[i for i in files if i.split('.')[1] == "bg"] for subdir, dirs, files in os.walk("Users")] if j])]

SPEED = 1


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


class Registry:
    """
    Class to test out the registry. Currently, storing system settings.
    """

    class Directory:
        """
        Class to create a Registry directory. Houses name.
        """

        def __init__(self, name: str = "default"):
            self.name = name

        def __repr__(self):
            return "Directory with name {name}".format(name=self.name)

    class Key:
        """
        Class to create a Registry key. Houses name.
        """

        def __init__(self, name: str = "default", value: str = "default"):
            self.name = name
            self.value = value

        def __repr__(self):
            return "Key with name {name} and value {value}".format(name=self.name, value=self.value)

    def __init__(self):
        """
        This method is to iteratively read through the registry and create a directory-key structure that is intuitive and easy to manipulate in memory.
        """
        for subdir, dirs, files in os.walk("System\\REGISTRY"):  # Iterating through the Registry folder.
            for file in files:
                if file[len(file) - 5:] == "svkey":  # Making sure the files are svkeys.
                    file = "{subdir}\\{file}".format(subdir=subdir, file=file)  # Specifying the file path + name.
                    value = list(open(file, "r"))[0]  # Acquiring the value of the key.
                    self.add_key(file[16:len(file) - 6], value)  # Using the add_key method to add the key!
            # Below code scrapped in favor of the new add_key method!
            # if subdir == "System\\REGISTRY":  # Excluding the root folder
            #     continue
            # dir_name = subdir[16:]  # Removing the root folder and replacing all backslashes with periods.
            # target = self
            # if "\\" in dir_name:  # If the directory is nested
            #     path = dir_name.split("\\")
            #     for i in range(len(path) - 1):
            #         target = target.__getattribute__(path[i])
            # dir_name = dir_name.rpartition("\\")[2]
            # target.__setattr__(dir_name, Registry.Directory(dir_name))
            # # exec('self.{svdir} = Registry.Directory("{svdir}")'.format(svdir=dir_name))  # Creating Directories for registry structure.
            # for file in files:  # Iterating through every file in the folder.
            #     key_name = ("{subdir}\\{file}".format(subdir=subdir, file=file)).replace("\\", ".")  # Acquiring the base name
            #     key_name = key_name[16:len(key_name) - 6]  # Polishing
            #     try:
            #         value = list(open("{subdir}\\{file}".format(subdir=subdir, file=file), "r"))[0]  # Acquiring the value of the key.
            #         exec('self.{svkey} = Registry.Key("{subdir}\\{file}", "{value}")'.format(svkey=key_name, subdir=subdir, file=file, value=value).replace("\\", "\\\\"))  # Creating and storing the key.
            #         continue
            #     except IndexError:
            #         returning("The registry could not be read. Please reboot and try again.", 3)
            #         break

    def add_key(self, key: str = "", value=0):
        """
        This is a method to add keys to the volatile registry stored in local memory.
        DANGER: There is no security for this method. Using this, anyone can add keys anywhere in the local registry.
        :param key: The key to add. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The value to set the new key to.
        :return: 0 if successful, 1 if the key exists, 2 if the key is not formatted correctly.
        """
        # key_name = "System\\REGISTRY\\{path}".format(path=key.replace('.', "\\"))
        try:
            self.__getattribute__(key)  # Try to find if the key exists.
            returning("That key already exists.", 2)
            return 1
        except AttributeError:  # If it doesn't exist...
            try:
                # First, iteratively create directories that aren't present.
                target = self
                path = key.split("\\")
                for i in range(len(path) - 1):
                    try:
                        target = target.__getattribute__(path[i])
                    except AttributeError:
                        target.__setattr__(path[i], Registry.Directory(path[i]))
                        target = target.__getattribute__(path[i])
                # Once necessary directories are made/found, create the key.
                key_name = path[len(path) - 1]
                target.__setattr__(key_name, Registry.Key(key_name, value))
                return 0
            except AttributeError:
                returning("The key is not formatted correctly.", 2)
                return 2
            #     exec('self.{key} = Registry.Key("{name}", "{value}")'.format(key=key, name=key_name, value=value).replace("\\", "\\\\"))
            #     # Creating and storing the key. The replacement is to fix escape characters.
            #     return 0
            # except AttributeError:  # If the directory doesn't exist or it's broken
            #     key2 = ""
            #     path = key.split('.')
            #     for i in range(len(path) - 1):
            #         key2 += path[i]
            #         try:
            #             exec("self.{directory}".format(directory=key2))
            #         except AttributeError:
            #             exec('self.{directory} = Registry.Directory("{name}")'.format(directory=key2, name=key2.rpartition(".")[2]))
            #         key2 += '.'
            #     try:
            #         key2 += path[len(path) - 1]
            #         exec('self.{key} = Registry.Key("{name}", "{value}")'.format(key=key, name=key_name, value=value).replace("\\", "\\\\"))
            #         return 0
            #     except AttributeError:
            #         returning("The key is not formatted correctly.", 2)
            #         return 2

    def get_key(self, key: str = ""):
        """
        This is a method to get values for keys in the volatile registry. This does not read from keys stored on the disk.
        :param key: The key whose value to get. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: The value of the key specified, 1 if the specified key is not a key, 2 if the key was not found.
        """
        try:
            target = self
            path = key.split("\\")
            for i in range(len(path) - 1):
                try:
                    target = target.__getattribute__(path[i])
                except AttributeError:
                    target.__setattr__(path[i], Registry.Directory(path[i]))
                    target = target.__getattribute__(path[i])
            key = target.__getattribute__(path[len(path) - 1])
            if key.__class__ == Registry.Key:
                return key.value
            else:
                returning("The specified key is not a key.", 2)
                return 1
        except AttributeError:
            returning("The specified key was not found.", 2)
            return 2

    def set_key(self, key: str = "", value: str = ""):
        try:
            target = self
            path = key.split("\\")
            for i in range(len(path) - 1):
                try:
                    target = target.__getattribute__(path[i])
                except AttributeError:
                    target.__setattr__(path[i], Registry.Directory(path[i]))
                    target = target.__getattribute__(path[i])
            key = target.__getattribute__(path[len(path) - 1])
            if key.__class__ == Registry.Key:
                key.__setattr__("value", value)
            else:
                returning("The specified key is not a key.", 2)
                return 1
        except AttributeError:
            returning("The specified key was not found.", 2)
            return 2

    def delete_key(self, key: str = ""):
        """
        This is a method to delete keys stored in the volatile registry. This does not delete keys stored on the disk.
        :param key: The key to delete. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: 0 if successful, 1 if the specified key is not a key, 2 if the key was not found.
        """
        try:
            target = self.__getattribute__(key)
            if target.__class__ == Registry.Key:
                self.__delattr__(key)
                return 0
            else:
                returning("The specified key is not a key.", 2)
                return 1
        except AttributeError:
            returning("The specified key was not found.", 2)
            return 2

    @staticmethod
    def modify_registry(key: str = "", path: str = "", value=0):
        """
        This is a method to modify the non-volatile registry keys stored on the local disk.
        DANGER: There is no security for this method. Using this, anyone can modify the registry and break the OS.
        :param key: The svkey file to modify.
        :param path: The path to the key.
        :param value: The new value for the key.
        :return: 0 if successful, 1 if unsuccessful.
        """
        try:
            key = (key + ".svkey") if ".svkey" not in key else key
            file = open("System\\REGISTRY\\{path}\\{key}".format(path=path, key=key), 'w')
            file.write(value)
            file.close()
            return 0
        except (FileNotFoundError, FileExistsError, OSError):
            returning("The registry cannot find the key specified. Please reboot and try again.", 3)
            return 1


# MARKER: INTERRUPTS
class HomeInterrupt(Exception):
    """
    Class HomeInterrupt. Houses the error to raise if the user wants to go home.
    """

    def __repr__(self):
        return "HomeInterrupt(Interrupt){}".format(self.args[0])


class LockInterrupt(Exception):
    """
    Class LockInterrupt. Houses the error to raise if the user wants to lock the screen.
    """

    def __repr__(self):
        return "LockInterrupt(Interrupt){}".format(self.args[0])


# MARKER: CUSTOM PRINT/INPUT
def pocs_print(message="", color=0):
    """
    Custom Print Method to print things with the correct color.
    :param message:
    :param color:
    :return:
    """
    print("\033[{}m{}".format((COLORS["red"] if color else 0), message))
    return


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
    suppress : Pass True to stop QTConsole from jumping when Space bar is pressed
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
                if to_reveal:
                    print("\b\u200c", end="", flush=True)
                else:
                    # Handling different length masking character
                    print(("\b" * mask_length) + ("\u200c" * mask_length),
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
                        print(("\b" * len(password_input)) +
                              ("\u200c" * len(password_input)),
                              end="", flush=True)
                        count = 0
                else:
                    # If the mask isn't "", then something has been
                    # printed on the screen, and we need to remove it
                    # before printing the previously entered text
                    if to_reveal:
                        print(("\b" * len(password_input) * mask_length) +
                              ("\u200c" * len(password_input) * mask_length) +
                              password_input, end="", flush=True)
                    else:
                        # Just removing the printed text and printing
                        # the mask character to unreveal the text.
                        print(("\b" * len(password_input)) +
                              (mask * len(password_input)), end="", flush=True)

            elif key == keyboard.Key.esc:
                password_input = ""
                return False

    def on_release(key):
        """
        Function only for detecting CTRL key release
        """
        nonlocal shift_hold
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
            shift_hold = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=suppress)
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
        if encrypted_h[i] == '\n':
            decrypted_h += '\n'
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
    if len(encrypted_h) < 100:
        return encrypted_h + '\\' + ''.join(random.choices(ALPHABET, k=99 - len(encrypted_h)))
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
