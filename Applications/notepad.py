"""
A note-writing application featuring note selection and deletion but no editing (yet).
AHA! The editing has finally come to notepad. BAM!
"""

import threading
import time

from Applications.cabinet import FileEngine

category = "utilities"
version = "3.1"
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

    def __repr__(self):
        return '(G)'.join(self.text)
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
            """
            Method to automatically type lines of notes from an existing file.
            :param delay: How much delay to give to regulate timings and keypresses.
            """
            time.sleep(delay)
            text = self.text[line]
            self.text[line] = ""
            controller.type(text)
        if self.text:
            print("Here's your note from last time:\n{}\n\n".format(self.__repr__().replace('(G)', '\n')))
            line = 0
            threading.Thread(target=type_line, args=(0.05,)).start()
        else:
            print("Type something! Use [Shift]+[ENTER] when you're done to save the file.")

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
        if input("\n\n# PREVIEW\n{}\n# PREVIEW\n\nWould you like to save your note?".format(self.__repr__().replace("(G)", "\n"))).lower() in ("save", "save note", "save my note", "yes", "absolutely"):
            FileEngine.quit(self, ".txt")
