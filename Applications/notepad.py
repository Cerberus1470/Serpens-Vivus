import time

from System import Loading
import os


# noinspection PyTypeChecker
class Notepad:
    def __init__(self):
        return

    def __repr__(self):
        return "< I am a Notepad class called " + self.__class__.__name__ + ">"

    def delete_note(self):
        pass

    def main(self, current_user):
        # Simple notes program that allows one to enter notes and save them to memory. Soon to be saved to disk.
        print("Welcome to notepad!\n")
        while True:
            new_file = False
            while True:
                for subdir, dirs, files in os.walk('Users\\%s' % current_user.username):
                    for file in files:
                        if file[len(file)-3:len(file)] == 'txt':
                            print(str(files.index(file)) + '. ' + file)
                    print(str(len(files)) + '. New Note')
                    print(str(len(files) + 1) + '. Delete Note')
                filename = input("Which file would you like to open?\n").lower()
                if filename == 'new note':
                    new_file = True
                    break
                elif filename == 'delete note':
                    self.delete_note()
                else:
                    try:
                        note = open('Users\\%s\\%s' % (current_user.username, filename), 'r')
                    except FileNotFoundError:
                        try:
                            note = open('Users\\%s\\%s' % (current_user.username, filename + '.txt'), 'r')
                            filename = filename + '.txt'
                        except FileNotFoundError:
                            print("Choose a valid option.")
                            time.sleep(1)
                            continue
                    print("Here is your note:")
                    for i in note:
                        print(Loading.caesar_decrypt(i.split('\n')[0]))
                    note.close()
                    break
            notes_temp = ''
            while True:
                print("\nType something!")
                notes_temp_section = input()
                neworsave = input('New line or Save the text file? Type "New Line" for a new line and "Save" to save the text and return to the homepage.')
                if notes_temp:
                    notes_temp += '\n' + notes_temp_section
                    pass
                else:
                    notes_temp = notes_temp_section
                    pass
                if neworsave.lower() in 'save file':
                    break
            if new_file:
                filename = input("File name?\n")
                note = open('Users\\%s\\%s.txt' % (current_user.username, filename), 'w')
                for i in notes_temp.split('\n'):
                    note.write(Loading.caesar_encrypt(i) + '\n')
                note.close()
            else:
                note = open('Users\\%s\\%s' % (current_user.username, filename), 'a')
                for i in notes_temp.split('\n'):
                    note.write(Loading.caesar_encrypt(i) + '\n')
                note.close()
            # if current_user.notes:
            #     current_user.notes += '\n' + notes_temp
            # else:
            #     current_user.notes = notes_temp
            if input('Type another note? Type "yes" to write something else or "no" to return to the applications screen.').lower() == 'yes':
                continue
            else:
                return
