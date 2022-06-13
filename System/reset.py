import time
from System import Loading
import os


class Reset:
    category = "admin"
    name = "Reset"

    @staticmethod
    def boot(os_object):
        os_object.current_user = os_object.current_user
        return Reset.user_reset()

    def __init__(self):
        return

    def __repr__(self):
        return "Reset"

    @staticmethod
    def user_reset():
        print('\n'*10)
        print("RESET ALL SETTINGS")
        if input("Type 'resetall' to continue or press [ENTER] or [return] to return to the applications screen.\n") == 'resetall':
            if input('Are you sure you want to reset all settings? This includes notes, users and their settings, game progress, and everything else. '
                     'Type "CONTINUE" to continue.\n') == 'CONTINUE':
                if input("This is your last chance. Reset all settings and return to setup? 'yes' or 'no'.") == 'yes':
                    Loading.returning("Quitting all programs...", 2)
                    print()
                    Loading.returning("Resetting Users...", 2)
                    for subdir, dirs, files in os.walk("Users"):
                        for i in files:
                            os.remove(subdir + '\\' + i)
                    for subdir, dirs, files in os.walk("Users"):
                        for i in dirs:
                            os.rmdir(subdir + "\\" + i)
                    os.rmdir("Users")
                    file = open('System\\event_log.info', 'w')
                    Loading.log("System reset.")
                    file.close()
                    del file
                    print("\nThe system has successfully reset and will restart shortly.")
                    time.sleep(2)
                    return 4
                else:
                    Loading.returning_to_apps()
                    return 0
            else:
                Loading.returning_to_apps()
                return 0
        else:
            Loading.returning_to_apps()
            return 0
