import time


class Reset:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a reset class named" + self.__class__.__name__ + ">"

    @staticmethod
    def user_reset(os):
        print('\n'*5)
        print("RESET ALL SETTINGS")
        print("\nAre you sure you want to reset all settings? This includes notes, users and their settings, game progress, and "
              "everything else.")
        print("Type 'resetall' to continue or press [ENTER] or [return] to return to the applications screen.")
        reset_choice = input()
        if reset_choice == 'resetall':
            print("Type your username to continue.")
            if input() == os.current_user.username:
                print("Type your password to continue.")
                if input() == os.current_user.password:
                    print("This is your last chance. Reset all settings and return to setup? 'yes' or 'no'.")
                    if input().lower() == 'yes':
                        time.sleep(2)
                        print("All programs quitted.")
                        time.sleep(2)
                        print("Username reset.")
                        time.sleep(2)
                        print("Password reset.")
                        time.sleep(2)
                        print("Notes reset.")
                        time.sleep(2)
                        print("Entering setup.")
                        time.sleep(2)
                        del os.current_user
                        del os.users
                        del os.versions
                        for i in range(100):
                            print("SETUP")
                        print()
                    else:
                        print("Returning to the applications screen!")
                        return
                else:
                    print("Incorrect password. Sending you back to the applications screen.")
                    time.sleep(3)
                    return
            else:
                print("Incorrect username. Sending you back to the applications screen.")
                time.sleep(3)
                return
        else:
            print("Returning to the applications screen!")
            time.sleep(3)
            return
