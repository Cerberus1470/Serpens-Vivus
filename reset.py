import time

import Loading


class Reset:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a reset class named" + self.__class__.__name__ + ">"

    @staticmethod
    def user_reset():
        print('\n'*10)
        print("RESET ALL SETTINGS")
        print("Type 'resetall' to continue or press [ENTER] or [return] to return to the applications screen.")
        reset_choice = input()
        if reset_choice == 'resetall':
            if input('Are you sure you want to reset all settings? This includes notes, users and their settings, game progress, and everything else. '
                     'Type "CONTINUE" to continue.\n') == 'CONTINUE':
                if input("This is your last chance. Reset all settings and return to setup? 'yes' or 'no'.").lower() == 'yes':
                    Loading.returning("Quitting all programs...", 2)
                    print()
                    Loading.returning("Resetting Users...", 2)
                    file = open('db_protected.txt', 'w')
                    file.close()
                    file = open('db_unprotected.txt', 'w')
                    file.close()
                    del file
                    print("\nThe system has successfully reset and will restart shortly.")
                    time.sleep(2)
                    return
                else:
                    Loading.returning("Returning to the applications screen!", 3)
                    return
            else:
                Loading.returning("Returning to the applications screen!", 3)
                return
        else:
            Loading.returning("Returning to the applications screen!", 3)
            return
