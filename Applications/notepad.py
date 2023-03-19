"""
A note-writing application featuring note selection and deletion but no editing (yet).
"""
from System import Loading
import os


# noinspection PyTypeChecker
class Notepad:
    """
    Class Notepad.
    Regulates the connections with Cerberus and organizes methods.
    """

    category = "utilities"

    @staticmethod
    def boot(os_object):
        """
        Used to regulate the bootup sequence for the game
        :param os_object: OS Object passed from Cerberus.
        :return: Nothing
        """
        while True:
            notepad = Notepad(os_object.current_user.username)
            if notepad.filename == 'exit':
                break
            else:
                if notepad.main(os_object.current_user.username) == 0:
                    break

    def __init__(self, username):
        self.username = username
        print("Welcome to Notepad!\n")
        self.new_file = False
        while True:
            for subdir, dirs, files in os.walk('Users\\%s' % self.username):
                count = 1
                for file in files:
                    if file[len(file) - 3:len(file)] == 'txt':
                        print(str(count) + '. ' + file)
                        count += 1
                print(str(count) + '. New Note')
                print(str(count + 1) + '. Delete Note')
            self.filename = input('Which file would you like to open? Type "exit" to exit.\n').lower()
            if self.filename == 'exit':
                self.filename = "exit"
                Loading.returning_to_apps()
                return
            if self.filename == 'new note':
                self.new_file = True
                break
            elif self.filename == 'delete note':
                self.delete_note(self.username)
            else:
                try:
                    note = open('Users\\%s\\%s' % (self.username, self.filename), 'r')
                except FileNotFoundError:
                    try:
                        note = open('Users\\%s\\%s' % (self.username, self.filename + '.txt'), 'r')
                        self.filename += '.txt'
                    except FileNotFoundError:
                        Loading.returning("Choose a valid option.", 1)
                        continue
                print("Here is your note:")
                for i in note:
                    print(Loading.caesar_decrypt(i.split('\n')[0]))
                note.close()
                break
        self.notes_temp = self.notes_temp_section = ''
        return

    def __repr__(self):
        return "< I am a Notepad class called " + self.__class__.__name__ + ">"

    @staticmethod
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

    def main(self, current_username):
        """
        Main method for the notepad program
        :param current_username: String to define the path to look in
        :return: 1 if the user wants to create or add to another note, 0 if they don't.
        """
        # Simple notes program that allows one to enter notes and save them to memory. Soon to be saved to disk.
        self.notes_temp = ''
        while True:
            if not self.notes_temp_section:
                print("\nType something!")
                self.notes_temp_section = Loading.pocs_input(app_object=self)
            new_or_save = Loading.pocs_input('New line or Save the text file? Type "New Line" for a new line and "Save" to save the text and return to the homepage.')
            if self.notes_temp:
                self.notes_temp += '\n' + self.notes_temp_section
                pass
            else:
                self.notes_temp = self.notes_temp_section
                pass
            if new_or_save.lower() in 'save file':
                break
        if self.new_file:
            filename = input("File name?\n")
            note = open('Users\\%s\\%s.txt' % (current_username, filename), 'w')
        else:
            note = open('Users\\%s\\%s' % (current_username, self.filename), 'a')
        for i in self.notes_temp.split('\n'):
            note.write(Loading.caesar_encrypt(i) + '\n')
        note.close()
        if input('Type another note? Type "yes" to write something else or "no" to return to the applications screen.').lower() == 'yes':
            return 1
        else:
            return 0
