import time
from jokes import Jokes
from notepad import Notepad
from task_manager import TaskManager
from user_settings import UserSettings
from system_info import SystemInfo
from User import Administrator
from reset import Reset


class OperatingSystem:

    def __init__(self, users):
        # Users and passwords
        self.users = users
        self.name = "Cerberus"
        self.versions = {"main": 11.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.12, "tictactoe": 1.10, "hangman": 1.8, "userset": 1.11, "sysinfo": 1.4}
        self.user_settings = UserSettings()
        # Setting current user and password
        for i in range(len(self.users)):
            try:
                self.users[i].notes
            except KeyError:
                self.users[i].notes[i] = ''
        for i in range(len(self.users)):
            if self.users[i].current:
                self.current_user = self.users[i]
                break
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    def startup(self):
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            print()
            # Label(main_window, text="Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.").grid(row=0, column=0)
            print("Hello! I am %s." % self.name)
            if self.current_user.username != 'Guest':
                # Separate while loop for users. Guest users head down.
                while True:
                    print("Current user: " + self.current_user.username + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
                    print("Enter password.")
                    pwd = input()
                    if pwd == self.current_user.password:
                        print("Welcome!")
                        os = self.operating_system()
                        if os == 2 or os == 3:
                            return
                        elif os == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        else:
                            return 'restart'
                    elif pwd == 'switch':
                        if len(self.users) > 1:
                            self.user_settings.switch_user(self, "os")
                            break
                        else:
                            print("There is currently only one user registered.")
                    elif pwd == 'shutdown':
                        shutdown = self.shutdown('db_protected.txt', 'db_unprotected.txt')
                        if shutdown == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        elif shutdown == 2 or shutdown == 3:
                            return
                        elif shutdown == 4:
                            return 'restart'
                        print("Hello! I am %s, running user: " % self.name + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
                    elif pwd == 'debugexit':
                        return
                    else:
                        print("Sorry, that's the wrong password. Try again.")
                        pass
            else:
                while True:
                    # The guest account, housed in its own while loop. The only way to exit is to use debugexit.
                    print("The Guest account will boot into the main screen, but any user settings will have no effect. This includes usernames, passwords, game progress, saved notes, etc. Press [ENTER] or [return] to login")
                    if input() == 'debugexit':
                        return
                    self.operating_system()
                    break

    def operating_system(self):
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        print("Hello! I am %s, running POCS v%s" % (self.name, self.versions["main"]))
        while True:
            print("\nAPPLICATIONS")
            print("1. Jokes")
            print("2. Notepad")
            print("3. Game: Bagels")
            print("4. Game: Tic-Tac-Toe")
            print("5. Game: Hangman")
            print("6. Game: Sonar")
            print("7. Task Manager")
            print("8. Change User Settings")
            print("9. System Info")
            print("10. Reset")
            print("11. Lock Computer")
            print("12. Shutdown")
            print("Select one from the list above.")
            choice = input().lower()
            # The if elif of choices... so long...
            if choice in ('jokes', 'joke', '1'):
                self.current_user.saved_state['Jokes'] = 'running'
                Jokes.main()
            elif choice in ('notepad', 'notes', 'note', '2'):
                self.current_user.saved_state['Notepad'] = 'running'
                self.current_user.notes = Notepad.main(self.current_user)
            elif choice in ('bagels', 'bagels', '3'):
                self.current_user.saved_state["Bagels Game"] = "running"
                self.current_user.bagels.main()
            elif choice in ('tictactoe', 'tic-tac-toe', 'ttt', '4'):
                self.current_user.saved_state["TicTacToe"] = "running"
                self.current_user.ttt.main()
            elif choice in ('hangman', '5'):
                self.current_user.saved_state["Hangman"] = "running"
                self.current_user.hangman.main()
            elif choice in ('sonar', '6'):
                print("Still in progress...")
            elif choice in ('task manager', '7'):
                TaskManager.main(self.current_user.saved_state)
            elif choice in ('user settings', 'usersettings', '8'):
                self.current_user.saved_state["User Settings"] = "running"
                self.user_settings.main(self)
            elif choice in ('system info', 'sys info', '9'):
                SystemInfo.main(self.versions)
            elif choice in ('reset', '10'):
                Reset.user_reset(self)
            elif choice in ('exit', 'lock computer', '11'):
                print("Computer has been locked.")
                return 'regular'
            elif choice in ('shutdown', '12'):
                return self.shutdown('db_protected.txt', 'db_unprotected.txt')
            elif choice in ('debugexit', 'debug'):
                return 'regular'
            else:
                print("Please choose from the list of applications.")

    def shutdown(self, protected_db_file, unprotected_db_file):
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file.
        # Exits safely after that.
        while True:
            print("Choose an option.")
            print("1. Sleep\n2. Hibernate\n3. Shutdown\n4. Restart\nType \"info\" for details.")
            shutdown_choice = input().lower()
            if shutdown_choice in "info":
                print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                      "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                      "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                      "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                      "the program again.")
                input()
                pass
            elif shutdown_choice in ("sleep", "1"):
                print("Sleeping...")
                return 1
            elif shutdown_choice in ("hibernate", "2", 'shutdown', '3', 'restart', '4'):
                hibernate = False
                shutdown = False
                if shutdown_choice in ('hibernate', '2'):
                    print("Hibernating...")
                    hibernate = True
                elif shutdown_choice in ('shutdown', '3', 'restart', '4'):
                    print("Shutting down will erase all game progress. Users and their notes will be saved. Are you sure you want to continue?")
                    if input("Type \"shutdown\" to continue, or press [ENTER] or [return] to return to the previous screen.") == 'shutdown':
                        pass
                    else:
                        print("Returning to the login screen in 3 seconds.")
                        time.sleep(3)
                        return 0
                    if shutdown_choice in ('shutdown', '3'):
                        shutdown = True
                        print("Shutting down...")
                    else:
                        print("Restarting...")
                    # Check if any programs are running
                    program_running = False
                    force_quit = 'shutdown'
                    for i in self.current_user.saved_state:
                        if self.current_user.saved_state[i] == 'running':
                            print("The " + i + " program is running.")
                            program_running = True
                    if program_running:
                        print("Would you like to force quit these apps? Type [ENTER] or [return] to return to the OS to save your progress. ")
                        force_quit = input("Type \"shutdown\" to force quit all apps and proceed with shutdown >>> ")
                    else:
                        print("No apps are open.")
                    if force_quit == 'shutdown':
                        pass
                    else:
                        # Return to allow the user to save their progress.
                        print("Returning to the login screen in 3 seconds.")
                        time.sleep(3)
                        return 0
                    if shutdown_choice in ('shutdown', '3'):
                        print("Shutting down...")
                    else:
                        print("Restarting...")
                    # Proceeding with force quitting and shutting down.
                    self.current_user.saved_state["Jokes"] = self.current_user.saved_state["Notepad"] = self.current_user.saved_state["Bagels Game"] = \
                        self.current_user.saved_state["TicTacToe"] = self.current_user.saved_state["User Settings"] = \
                        self.current_user.saved_state["System Info"] = "not running"
                # Much is similar to shutting down, except no force quitting.
                # First open the databases.
                protected_db = open(protected_db_file, 'w')
                unprotected_db = open(unprotected_db_file, 'w')
                # Append each user, password, and current status to the lists.
                for i in self.users:
                    # # Try to access everyone's notes. If it doesn't exist, give them an empty notes string.
                    try:
                        # Special protocol to translate all new lines to tabs for notes db formatting.
                        while '\n' in i.notes:
                            (notes1, notes2) = i.notes.split('\n', 1)
                            i.notes = notes1 + '\t' + notes2
                    except (KeyError, ValueError):
                        i.notes = ''
                    if hibernate:
                        # Try accessing ttt progress... if not, say nothing.
                        # Special protocol to translate ttt progress lists and strings to strings with splitters for db formatting.
                        translated_board = ''
                        for j in range(8):
                            if i.ttt.board[j] == 'X' or i.ttt.board[j] == 'O':
                                translated_board += (i.ttt.board[j] + ',')
                            else:
                                translated_board += ' ,'
                        # Append user-specific to the list
                        i.ttt = translated_board + '.' + str(i.ttt.turn) + '.' + i.ttt.player_letter

                        # Now for bagels!
                        # Simple Array, no translation needed.
                        i.bagels = i.bagels.last_guess + '.' + i.bagels.num_guesses + '.' + i.bagels.num_digits + '.' + i.bagels.secret_num + '.' + i.bagels.max_guesses
                        # Now to store each user's open apps.

                        # Now for hangman!
                        i.hangman = i.hangman.missed_letters + '.' + i.hangman.correct_letters + '.' + i.hangman.secret_word + '.' + i.hangman.secret_key

                        # Running Programs!
                        translated_save_state = ''
                        for j in i.saved_state:
                            # noinspection PyTypeChecker
                            translated_save_state += i.saved_state[j] + '.'
                        i.saved_state = translated_save_state[0:len(translated_save_state)-1]
                        # After translation and empty notes creation, add everything to the notes list to write to the db later.
                # Then write each user, password, and current status to the database, saving it to disk.
                # Also write the notes to the database.
                for i in self.users:
                    protected_db.write(str(i).split('\n', 1)[1] + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + "\t\t" + i.notes + '\t\t\n')
                    if hibernate:
                        unprotected_db.write(i.username + '\t\t' + i.ttt + '\t\t' + i.bagels + '\t\t' + i.hangman + '\t\t' + i.saved_state + '\t\t\n')
                    else:
                        pass
                # Close the databases.
                protected_db.close()
                unprotected_db.close()
                if hibernate:
                    input("Hibernation complete. Open \"%s.py\" to restart the system." % self.name)
                    return 2
                elif shutdown:
                    input("Shutdown complete. Open \"%s.py\" to restart the system." % self.name)
                    return 3
                else:
                    print("Restarting system...")
                    time.sleep(2)
                    print("Booting...")
                    time.sleep(2)
                    return 4

    def setup(self):
        # The setup method. Conveniently sets up the system to run on its first bootup. Modifies the dictionary with a new user.
        print("SETUP: Since this is the first time you're running this OS, you have entered the setup.")
        # Ask the user if they want to make a user or not.
        print("Would you like to create a new user, or login as guest?")
        user_or_guest = input()
        if user_or_guest.lower() in ('new user', 'new', 'user', 'yes'):
            # New user it is!
            print("Name your user:")
            setup_user = input()
            print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
            while True:
                # The while loop handles the password creation. Can only escape under certain circumstances.
                setup_pwd = input()
                if setup_pwd:
                    # If the user entered a password:
                    print("Password set. Enter it again to confirm it.")
                    if setup_pwd == input():
                        break
                    else:
                        # Handle password matching. Loops back to ensure the user typed the correct passwords.
                        print('The passwords you entered didn\'t match. Type the same password twice.')
                else:
                    # If the user did not enter a password:
                    self.current_user = Administrator(setup_user, 'python123', True, '')
                    self.users.append(self.current_user)
                    print('Default password set. The password is "python123". Entering startup in 3 seconds.')
                    time.sleep(3)
                    return
            # User entered password correctly twice.
            self.current_user = Administrator(setup_user, setup_pwd, True, '')
            self.users.append(self.current_user)
            print("Password set successfully. Entering startup in 3 seconds.")
            time.sleep(3)
            return
        else:
            # If the user did not specify whether or not they wanted a new user.
            self.current_user = Administrator("Guest", "", True, '')
            self.users.append(self.current_user)
            print("Guest user added. There is no password. Press [ENTER] or [return] during login. Entering startup in 3 seconds.")
            time.sleep(3)
            return
