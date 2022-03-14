class Notepad:
    def __init__(self):
        return

    def __repr__(self):
        return "< I am a Notepad class called " + self.__class__.__name__ + ">"

    @staticmethod
    def main(current_user):
        # Simple notes program that allows one to enter notes and save them to memory. Soon to be saved to disk.
        print("Welcome to notepad! Type out anything you want! Here are your notes from last time (if it's empty, you don't have any notes!)")
        print(current_user.notes)
        notes_temp = ''
        while True:
            print("Type something!")
            notes_temp_section = input()
            print('New line or Save the text file? Type "New Line" for a new line and "Save" to save the text and '
                  'return to the homepage.')
            neworsave = input()
            if notes_temp:
                notes_temp += '\n' + notes_temp_section
            else:
                notes_temp = notes_temp_section
            if neworsave.lower() == 'save' or neworsave.lower() == 'save file':
                if current_user.notes:
                    current_user.notes += '\n' + notes_temp
                else:
                    current_user.notes = notes_temp
                print("Press [ENTER] or [return] to return to the applications screen!")
                input()
                return
