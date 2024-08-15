"""
A note-writing application featuring note selection and deletion but no editing (yet).
"""

import os
import threading
import time

from Applications.cabinet import FileEngine
from System import Loading

category = "utilities"
version = "3.0"
entries = ('notepad', 'notes', 'note', '2')


def boot(os_object=None):
    """
    Used to regulate the bootup sequence for the game
    :param os_object: OS Object passed from Cerberus.
    :return: Nothing
    """
    while True:
        notepad = Notepad(os_object.path.format(os_object.current_user.username))
        if notepad.filename != 'exit':
            notepad.main()
        else:
            break


# noinspection PyTypeChecker
class Notepad:
    """
    Class Notepad.
    Regulates the connections with Cerberus and organizes methods.
    """

    def __init__(self, path="\\", text=""):
        self.new_file = False
        self.path = path
        self.filename = ''
        self.text = text if text else FileEngine.init(self, self.path, 'txt')
        self.text = self.text if self.text else [""]

        return

        # print("Welcome to Notepad!\n")
        # self.new_file = False
        # while True:
        #     count = 1
        #     for subdir, dirs, files in os.walk(path):
        #         for file in files:
        #             if file[len(file) - 3:len(file)] == 'txt':
        #                 print(str(count) + '. ' + file)
        #                 count += 1
        #     print(str(count) + '. New Note')
        #     print(str(count + 1) + '. Delete Note')
        #     self.filename = input('Which file would you like to open? Type "exit" to exit.\n').lower()
        #     if self.filename == 'exit':
        #         self.filename = "exit"
        #         Loading.returning_to_apps()
        #         return
        #     if self.filename == 'new note':
        #         self.new_file = True
        #         break
        #     elif self.filename == 'delete note':
        #         self.delete_note(self.username)
        #     else:
        #         try:
        #             note = open('Users\\%s\\%s' % (self.username, self.filename), 'r')
        #         except FileNotFoundError:
        #             try:
        #                 note = open('Users\\%s\\%s' % (self.username, self.filename + '.txt'), 'r')
        #                 self.filename += '.txt'
        #             except FileNotFoundError:
        #                 Loading.returning("Choose a valid option.", 1)
        #                 continue
        #         print("Here is your note:")
        #         for i in note:
        #             print(Loading.caesar_decrypt(i.split('\n')[0]))
        #         note.close()
        #         break
        # self.notes_temp = self.notes_temp_section = ''
        # return

    def __repr__(self):
        return '\n'.join(self.text)
        # return "< I am a Notepad class called " + self.__class__.__name__ + ">"

    def __getstate__(self):
        return "Notepad(SS1){}".format(self.text)

    def main(self):
        """
        Main method for the notepad program
        :return: 1 if the user wants to create or add to another note, 0 if they don't.
        Pseudocode: Each line will be edited individually, and stored individually in a list. Typing is normal, enter moves to the next line. Using the
        up/down arrow keys will switch between lines. Printing will look weird, but it should be intuitive enough to display properly. Let's see...
        """
        # Simple notes program that allows one to enter notes and save them to memory. Soon to be saved to disk.
        from pynput import keyboard
        shift_hold = False
        controller = keyboard.Controller()

        def type_line(delay):
            time.sleep(delay)
            text = self.text[line]
            self.text[line] = ""
            controller.type(text)
            # for i in self.text.split('\n'):
            #     controller.type(i)
            #     controller.press(keyboard.Key.shift_l)
            #     controller.tap(keyboard.Key.enter)
            #     controller.release(keyboard.Key.shift_l)
        if self.text:
            print("Here's your note from last time:\n{}\n\n".format(self))
            line = 0
            threading.Thread(target=type_line, args=(0.05,)).start()
        else:
            print("Type something! Use [Shift]+[ENTER] when you're done to save the file.")
        # self.text = input().replace('\n', '(n)')
        # while True:
        #     line = input().replace('\n', '(n)')
        #     if line:
        #         self.text += line
        #     else:
        #         self.text += '\n'
        # I want to swap shift-enter (new line) and enter (submit input) behaviors.

        def on_press(key):
            """
            Method to handle keypresses. Only need to handle keys, shift, and enter.
            :param key: The key pressed. Type pynput.keyboard.Key.
            :return: False to stop the Listener.
            """
            nonlocal shift_hold, controller, line
            try:
                self.text[line] += upper(key.char) if shift_hold else key.char
                print(upper(key.char) if shift_hold else key.char, end="", flush=True)
            except AttributeError:
                if key == keyboard.Key.space:
                    self.text[line] += " "
                    print(" ", end="", flush=True)
                if key in [keyboard.Key.shift_r, keyboard.Key.shift_l]:
                    shift_hold = True
                if key == keyboard.Key.enter:
                    if shift_hold:
                        return False
                    else:
                        self.text.insert(line + 1, '')
                        line += 1
                        print()
                elif key == keyboard.Key.backspace:
                    if self.text[line]:
                        self.text[line] = self.text[line][:-1]
                        print("\b \b", end="", flush=True)  # \b only moves the cursor back, so we go back, print a space, then go back again.
                    else:
                        self.text.pop(line)
                        line -= 1
                        type_line(0)
                elif key in (keyboard.Key.up, keyboard.Key.down):
                    old_line = line
                    line += (1 if line != len(self.text) - 1 else 0) if key == keyboard.Key.down else (-1 if line != 0 else 0)
                    if old_line != line:
                        type_line(0)
                        print()

        def on_release(key):
            """
            Function only for detecting SHIFT key release
            """
            nonlocal shift_hold
            if key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
                shift_hold = False

        def upper(char):
            """
            Custom method to return capitalized letters of all keyboard keys.
            :param char:
            :return:
            """
            if char in 'abcdefghijklmnopqrstuvwxyz':
                return char.upper()
            elif char in '1234567890-=[]\\;\',./`':
                return '!@#$%^&*()_+{}|:\"<>?~'['1234567890-=[]\\;\',./`'.index(char)]

        listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
        listener.start()
        try:
            listener.join()
        except KeyboardInterrupt:
            pass
        listener.stop()
        if input("\n\n# PREVIEW\n{}\n# PREVIEW\n\nWould you like to save your note?".format(self)).lower() in ("save", "save note", "save my note", "yes", "absolutely"):
            FileEngine.quit_game(self, ".txt")

        # self.notes_temp = ''
        # while True:
        #     if not self.notes_temp_section:
        #         print("\nType something!")
        #         self.notes_temp_section = Loading.pocs_input(app_object=self)
        #     new_or_save = Loading.pocs_input('New line or Save the text file? Type "New Line" for a new line and "Save" to save the text and return to the homepage.')
        #     if self.notes_temp:
        #         self.notes_temp += '\n' + self.notes_temp_section
        #         pass
        #     else:
        #         self.notes_temp = self.notes_temp_section
        #         pass
        #     if new_or_save.lower() in 'save file':
        #         break
        # if self.new_file:
        #     filename = input("File name?\n")
        #     note = open('Users\\%s\\%s.txt' % (current_username, filename), 'w')
        # else:
        #     note = open('Users\\%s\\%s' % (current_username, self.filename), 'a')
        # for i in self.notes_temp.split('\n'):
        #     note.write(Loading.caesar_encrypt(i) + '\n')
        # note.close()
        # if input('Type another note? Type "yes" to write something else or "no" to return to the applications screen.').lower() == 'yes':
        #     return 1
        # else:
        #     return 0

    @staticmethod
    @DeprecationWarning
    def delete_note(current_username):
        """
        Method to regulate deleting notes
        :param current_username: String to define the path to look.
        :return: Nothing.
        """
        while True:
            for subdir, dirs, files in os.walk('Users\\%s' % current_username):
                count = 0
                for file in files:
                    if file[len(file) - 3:len(file)] == 'txt':
                        count += 1
                        print(str(count) + '. ' + file)
            delete_game = input("Which game would you like to delete?\n")
            try:
                os.remove("Users\\{}\\{}".format(current_username, delete_game))
                Loading.returning("The file was successfully deleted.", 2)
            except FileNotFoundError:
                try:
                    Loading.returning("The file was successfully deleted.", 2)
                    os.remove("Users\\{}\\{}".format(current_username, delete_game + ".txt"))
                    pass
                except FileNotFoundError:
                    Loading.returning("That file was not found.", 1)
                    pass
            if input('Delete another file? "Yes" or "No".').lower() == 'yes':
                continue
            else:
                return
