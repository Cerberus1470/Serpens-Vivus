class Notepad:
    def __init__(self):
        return

    def __repr__(self):
        return "< I am a Notepad class called " + self.__class__.__name__ + ">"

    @staticmethod
    def main(notes, stats, current_user):
        stats["Notepad"] = 'running'
        #Simple notes program that allows one to enter notes and save them to memory. Soon to be saved to disk.
        print("Welcome to notepad! Type out anything you want! Please don't use '\n', it will break the interface. A fix is coming"
              " soon. Instead, use the new line function: Press [ENTER] or [return] and type \"new line\"\nHere are your notes from"
              " last time (if it's empty, you don't have any notes!)")
        print(str(notes[current_user]))
        notes_temp = ''
        while True:
            notes_temp_section = input()
            print("New line or Save the text file? Type \"New Line\" for a new line and \"Save\" to save the text and "
                  "return to the homepage.")
            neworsave = input()
            notes_temp += '\n' + notes_temp_section
            if neworsave.lower() == 'save' or neworsave.lower() == 'save file':
                notes[current_user] += '\n' + notes_temp
                print("Press [ENTER] or [return] to return to the applications screen!")

                input()
                return notes
