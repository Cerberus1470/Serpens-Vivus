import time
from jokes import Jokes
from notepad import Notepad
from bagels import Bagels
from tictactoe import TicTacToe
from hangman import Hangman
from task_manager import TaskManager
from user_settings import UserSettings
from system_info import SystemInfo
from reset import Reset


class User:
    # Remove a space after a comma to reformat the file.

    def __init__(self, username, password, current, notes):
        self.username = username
        self.password = password
        self.current = current
        self.notes = notes
        return

    def __repr__(self):
        return "I am a user named " + self.username

    def __setGames__(self, bagels_game, ttt_game, hangman_game, state):
        self.bagels = bagels_game
        self.ttt = ttt_game
        self.hangman = hangman_game
        self.saved_state = state
        return


class OperatingSystem:

    def __init__(self, users):
        # Users and passwords
        self.users = users
        self.versions = {"main": 10.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.9, "tictactoe": 1.8, "hangman": 1.6, "userset": 1.5, "sysinfo": 1.3}
        self.user_settings = UserSettings()
        # Setting current user and password
        for i in range(len(self.users)):
            try:
                self.users[i].notes
            except KeyError:
                self.users[i].notes[i] = ''
        for i in range(len(self.users)):
            if self.users[i].current == 'CURRENT':
                self.current_user = self.users[i]
                break
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.__class__.__name__ + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    def startup(self):
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            print()
            # Label(main_window, text="Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.").grid(row=0, column=0)
            print("Hello! I am Cerberus, running user: " + self.current_user.username + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
            if self.current_user.username != 'Guest':
                # Separate while loop for users. Guest users head down.
                while True:
                    print("Enter password.")
                    pwd = input()
                    if pwd == self.current_user.password:
                        print("Welcome!")
                        os = self.operating_system()
                        if os in ('shutdown', 'hibernate'):
                            return
                        elif os in 'sleep':
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        else:
                            pass
                    elif pwd == 'switch':
                        if len(self.users) > 1:
                            (self.current_user.username, self.current_user.password) = OperatingSystem.userSettings.switch_user(self.users, self.current_user.username, self.current_user.password, 'os')
                            break
                        else:
                            print("There is currently only one user registered.")
                    elif pwd == 'shutdown':
                        shutdown = self.shutdown('userpwd_db.txt', 'user_notes.txt', 'saved_state.txt', self.users, self.notes, self.bagels_prog, self.ttt_prog, self.hangman_prog)
                        if shutdown == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        elif shutdown == 2 or shutdown == 3:
                            return
                        elif shutdown == 4:
                            return 'restart'
                        print("Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
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
        print("Hello! I am %s, running POCS v%s" % ("Cerberus", self.versions["main"]))
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
                Jokes.main()
                self.current_user.saved_state['Jokes'] = 'running'
            elif choice in ('notepad', 'notes', 'note', '2'):
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
                shutdown = self.shutdown('userpwd_db.txt', 'user_notes.txt', 'saved_state.txt', self.users, self.notes, self.bagels_prog, self.ttt_prog, self.hangman_prog)
                if shutdown == 1:
                    return 'sleep'
                elif shutdown == 2:
                    return 'hibernate'
                elif shutdown == 3:
                    return 'shutdown'
                else:
                    pass
            elif choice in ('debugexit', 'debug'):
                return 'regular'
            else:
                print("Please choose from the list of applications.")

    def shutdown(self, db_filename, notes_db, saved_state_db, dictionary, notes_dictionary, bagels_prog, ttt_prog, hangman_prog):
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
                if shutdown_choice in ('restart', '4'):
                    shutdown = True
                if shutdown:
                    print("Shutting down will erase all game progress. Users and their notes will be saved. Are you sure you want to continue?")
                    if input("Type \"shutdown\" to continue, or press [ENTER] or [return] to return to the previous screen >>> ") == 'shutdown':
                        pass
                    else:
                        print("Returning to the login screen in 3 seconds.")
                        time.sleep(3)
                        return 0
                    print("Shutting down...")
                    # Aesthetic pause...
                    time.sleep(2)
                    # Check if any programs are running
                    program_running = False
                    force_quit = 'shutdown'
                    for i in self.save_state[self.current_user]:
                        if self.save_state[self.current_user][i] == 'running':
                            print("The " + i + " program is running.")
                            program_running = True
                    if program_running:
                        print("Would you like to force quit these apps? Type [ENTER] or [return] to return to the OS to save your progress. ")
                        force_quit = input("Type \"shutdown\" to force quit all apps and proceed with shutdown >>> ")
                    else:
                        print("No apps are open.")
                        # Another aesthetic pause...
                        time.sleep(2)
                    if force_quit == 'shutdown':
                        pass
                    else:
                        # Return to allow the user to save their progress.
                        print("Returning to the login screen in 3 seconds.")
                        time.sleep(3)
                        return 0
                    print("Shutting down...")
                    # Proceeding with force quitting and shutting down.
                    self.save_state["Jokes"] = self.save_state["Notepad"] = self.save_state["Bagels Game"] = self.save_state["TicTacToe"] = self.save_state["User Settings"] = \
                        self.save_state["System Info"] = "not running"
                if shutdown_choice in ("hibernate", "2"):
                    print("Hibernating...")
                    hibernate = True
                # Much is similar to shutting down, except no force quitting.
                # First open the databases.
                db = open(db_filename, 'w')
                notes_db = open(notes_db, 'w')
                saved_state_db = open(saved_state_db, 'w')
                # Ready the lists.
                users = []
                passwords = []
                current = []
                notes = []
                bagels = []
                ttt = []
                hangman = []
                state = []
                # Append each user, password, and current status to the lists.
                for i in dictionary:
                    users.append(i)
                    passwords.append(dictionary[i][0])
                    current.append(dictionary[i][1])
                    # Try to access everyone's notes. If it doesn't exist, give them an empty notes string.
                    try:
                        # Special protocol to translate all new lines to tabs for notes db formatting.
                        while '\n' in notes_dictionary[i]:
                            (notes1, notes2) = notes_dictionary[i].split('\n', 1)
                            notes_dictionary[i] = notes1 + '!' + notes2
                    except (KeyError, ValueError):
                        notes_dictionary[i] = ''
                    if hibernate:
                        # Try accessing ttt progress... if not, say nothing.
                        # Special protocol to translate ttt progress lists and strings to strings with splitters for db formatting.
                        ttt_user_prog = ''
                        for j in range(8):
                            if ttt_prog[i][0][j] == 'X' or ttt_prog[i][0][j] == 'O':
                                ttt_user_prog += (ttt_prog[i][0][j] + ',')
                            else:
                                ttt_user_prog += ' ,'
                        # Append user-specific to the list
                        ttt_user_prog += ttt_prog[i][0][len(ttt_prog[i][0]) - 1] + '.' + ttt_prog[i][1] + '.' + ttt_prog[i][2]

                        # Now for bagels!
                        # Simple Array, no translation needed.
                        bagels_user_prog = ''
                        for j in range(4):
                            bagels_user_prog += str(bagels_prog[i][j]) + '.'
                        bagels_user_prog += str(bagels_prog[i][4])
                        # Now to store each user's open apps.

                        # Now for hangman!
                        hangman_user_prog = ''
                        for j in range(3):
                            hangman_user_prog += str(hangman_prog[i][j]) + '.'
                        hangman_user_prog += str(hangman_prog[i][3])
                        user_state = ''
                        for j in self.save_state[i]:
                            user_state += self.save_state[i][j] + '.'
                        # After translation and empty notes creation, add everything to the notes list to write to the db later.
                        notes.append(notes_dictionary[i])
                        ttt.append(ttt_user_prog)
                        bagels.append(bagels_user_prog)
                        hangman.append(hangman_user_prog)
                        state.append(user_state)
                # Then write each user, password, and current status to the database, saving it to disk.
                # Also write the notes to the database.
                for i in range(len(dictionary)):
                    db.write(users[i] + '\t\t' + passwords[i] + '\t\t' + current[i])
                    notes_db.write(users[i] + '\t\t' + notes[i] + '\t\t\n')
                    if hibernate:
                        saved_state_db.write(users[i] + '\t\t' + state[i] + '\t\t' + bagels[i] + '\t\t' + ttt[i] + '\t\t' + hangman[i] + '\t\t\n')
                    else:
                        saved_state_db.write(users[i] + '\t\tnot running.not running.not running.not running.not running.not running.\t\t . . . . \t\t , , , , , , , , . . \t\t . . . \t\t\n')
                # Close the databases.
                db.close()
                notes_db.close()
                saved_state_db.close()
                time.sleep(5)
                if hibernate:
                    input("Hibernation complete. Open \"Cerberus.py\" to restart the system.")
                    return 2
                elif shutdown:
                    input("Shutdown complete. Open \"Cerberus.py\" to restart the system.")
                    return 3
                else:
                    print("Restarting system...")
                    time.sleep(3)
                    return 4
            elif shutdown_choice in ("lol", 'testing'):
                print("Shutting down will erase all game progress. Users and their notes will be saved. Are you sure you want to continue?")
                if input("Type \"shutdown\" to continue, or press [ENTER] or [return] to return to the previous screen >>> ") == 'shutdown':
                    pass
                else:
                    print("Returning to the login screen in 3 seconds.")
                    time.sleep(3)
                    return 0
                print("Shutting down...")
                # Aesthetic pause...
                time.sleep(2)
                # Check if any programs are running
                program_running = False
                force_quit = 'shutdown'
                for i in self.save_state[self.current_user]:
                    if self.save_state[self.current_user][i] == 'running':
                        print("The " + i + " program is running.")
                        program_running = True
                if program_running:
                    print("Would you like to force quit these apps? Type [ENTER] or [return] to return to the OS to save your progress. ")
                    force_quit = input("Type \"shutdown\" to force quit all apps and proceed with shutdown >>> ")
                else:
                    print("No apps are open.")
                    # Another aesthetic pause...
                    time.sleep(2)
                if force_quit == 'shutdown':
                    pass
                else:
                    # Return to allow the user to save their progress.
                    print("Returning to the login screen in 3 seconds.")
                    time.sleep(3)
                    return 0
                print("Shutting down...")
                # Proceeding with force quitting and shutting down.
                self.save_state["Jokes"] = self.save_state["Notepad"] = self.save_state["Bagels Game"] = self.save_state["TicTacToe"] = self.save_state["User Settings"] = \
                    self.save_state["System Info"] = "not running"
                # First open the databases.
                db = open(db_filename, 'w')
                notes_db = open(notes_db, 'w')
                saved_state_db = open(saved_state_db, 'w')
                # Ready the lists.
                users = []
                passwords = []
                current = []
                notes = []
                # Append each user, password, and current status to the lists.
                for i in dictionary:
                    users.append(i)
                    passwords.append(dictionary[i][0])
                    current.append(dictionary[i][1])
                for i in dictionary:
                    # Try to access everyone's notes. If it doesn't exist, give them an empty notes string.
                    try:
                        # Special protocol to translate all new lines to tabs for notes db formatting.
                        while '\n' in notes_dictionary[i]:
                            (notes1, notes2) = notes_dictionary[i].split('\n', 1)
                            notes_dictionary[i] = notes1 + '!' + notes2
                    except KeyError:
                        notes_dictionary[i] = ''
                    # Try accessing ttt progress... if not, say nothing.
                    # Special protocol to translate ttt progress lists and strings to strings with splitters for db formatting.
                    pass
                    # After translation and empty notes creation, add everything to the notes list to write to the db later.
                    notes.append(notes_dictionary[i])
                # Then write each user, password, and current status to the database, saving it to disk.
                # Also write the notes to the database, and empty save states.
                for i in range(len(dictionary)):
                    db.write(users[i] + '\t\t' + passwords[i] + '\t\t' + current[i])
                    notes_db.write(users[i] + '\t\t' + notes[i] + '\t\t\n')
                    saved_state_db.write(users[i] + '\t\tnot running.not running.not running.not running.not running.not running.\t\t . . . . \t\t , , , , , , , , . . \t\t . . . \t\t\n')
                # Close the databases.
                db.close()
                notes_db.close()
                saved_state_db.close()
                time.sleep(5)
                print("Shut down complete.")
                # Fun ride back home!
                return 3

    def setup(self, dictionary):
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
                    self.current_user = setup_user
                    self.current_password = 'python123'
                    print('Default password set. The password is "python123". Entering startup in 3 seconds.')
                    time.sleep(3)
                    return
            # User entered password correctly twice.
            self.current_user = setup_user
            self.current_password = setup_pwd
            dictionary[0] = self.current_user, self.current_password, 'CURRENT\n'
            self.bagels_prog[0] = [' ', ' ', ' ', ' ', ' ']
            self.hangman_prog[0] = [' ', ' ', ' ', ' ']
            self.notes[0] = ' '
            print("Password set successfully. Entering startup in 3 seconds.")
            time.sleep(3)
            return
        else:
            # If the user did not specify whether or not they wanted a new user.
            self.current_user = 'Guest'
            print("Guest user added. There is no password. Press [ENTER] or [return] during login. Entering startup in 3 seconds.")
            time.sleep(3)
            return
