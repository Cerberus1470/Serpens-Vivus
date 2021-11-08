import time
from jokes import Jokes
from notepad import Notepad
from bagels import Bagels
from tictactoe import TicTacToe
from task_manager import TaskManager
from user_settings import UserSettings
from system_info import SysInfo
from reset import Reset


class OperatingSystem:
    # Initializing all class attributes for apps
    jokes = Jokes()
    notepad = Notepad()
    bagelsGame = Bagels()
    tictactoeGame = TicTacToe()
    taskManager = TaskManager()
    userSettings = UserSettings()
    systemInfo = SysInfo()
    reset = Reset()

    def __init__(self, args):
        # Initialize all instance attributes.
        # Current user and password
        self.current_user = ''
        self.current_password = ''
        # Users and passwords
        self.dictionary = args[0]
        # Notes from each user
        self.notes = args[1]
        # Bagels Progress
        self.bagels_prog = args[2]
        # TTT progress
        self.ttt_prog = args[3]
        # Setting current user and password
        for i in self.dictionary:
            try:
                temp = self.notes[i][0]
                del temp
            except KeyError:
                self.notes[i] = ''
        for i in self.dictionary:
            if self.dictionary[i][1] == 'CURRENT\n':
                self.current_user = i
                self.current_password = self.dictionary[i][0]
                break
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.__class__.__name__ + "\n Users: " + str(len(self.dictionary)) + "\n Current User: " + self.current_user + "\n Current Password is hidden. >"

    def operating_system(self, osname, versions, stats):
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        print("Hello! I am %s, running POCS v%s" % (osname, versions["main"]))
        while True:
            print("\nAPPLICATIONS")
            print("1. Jokes")
            print("2. Notepad")
            print("3. Game: Bagels")
            print("4. Game: Tic-Tac-Toe")
            print("5. Task Manager")
            print("6. Change User Settings")
            print("7. System Info")
            print("8. Reset")
            print("9. Lock Computer")
            print("10. Shutdown")
            print("Select one from the list above or press [ENTER] or [return] to lock!")
            choice = input()
            # The if elif of choices... so long...
            if choice.lower() in ('jokes', 'joke', '1'):
                OperatingSystem.jokes.main(stats)
            elif choice.lower() in ('notepad', 'notes', 'note', '2'):
                self.notes = OperatingSystem.notepad.main(self.notes, stats, self.current_user)
            elif choice.lower() in ('bagels', 'bagels', '3'):
                self.bagels_prog[self.current_user] = OperatingSystem.bagelsGame.main(stats, self.bagels_prog, self.current_user)
            elif choice.lower() in ('tictactoe', 'tic-tac-toe', 'ttt', '4'):
                self.ttt_prog[self.current_user] = OperatingSystem.tictactoeGame.main(stats, self.ttt_prog, self.current_user)
            elif choice.lower() in ('task manager', '5'):
                OperatingSystem.taskManager.main(stats)
            elif choice.lower() in ('user settings', 'usersettings', '6'):
                (self.current_user, self.current_password) = OperatingSystem.userSettings.main(self.current_user, self.current_password, self.dictionary, stats)
            elif choice.lower() in ('system info', 'sys info', '7'):
                OperatingSystem.systemInfo.main(stats, versions)
            elif choice.lower() in ('reset', '8'):
                OperatingSystem.reset.user_reset(self, self.current_user, self.current_password, stats)
            elif choice.lower() in ('exit', 'lock computer', '9'):
                print("Computer has been locked.")
                return
            elif choice.lower() in ('shutdown', '10'):
                shutdown = self.shutdown('userpwd_db.txt', 'user_notes.txt', self.dictionary, self.notes, self.bagels_prog, self.ttt_prog, stats)
                if shutdown == 1:
                    return 'sleep'
                elif shutdown == 2:
                    return 'hibernate'
                elif shutdown == 3:
                    return 'shutdown'
                else:
                    pass
            elif choice.lower() in 'debugexit':
                return
            else:
                print("Please choose from the list of applications.")

    def startup(self, versions, stats):
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            print()
            # Label(main_window, text="Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.").grid(row=0, column=0)
            print("Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
            if self.current_user != 'Guest':
                # Separate while loop for users. Guest users head down.
                while True:
                    print("Enter password.")
                    pwd = input()
                    if pwd == self.current_password:
                        print("Welcome!")
                        if self.operating_system("Cerberus", versions, stats) in ('shutdown', 'hibernate'):
                            return
                        else:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                    elif pwd == 'switch':
                        if len(self.dictionary) > 1:
                            (self.current_user, self.current_password) = OperatingSystem.userSettings.switch_user(self.dictionary, self.current_user, self.current_password, 'os')
                            break
                        else:
                            print("There is currently only one user registered.")
                    elif pwd == 'shutdown':
                        shutdown = self.shutdown('userpwd_db.txt', 'user_notes.txt', self.dictionary, self.notes, self.bagels_prog, self.ttt_prog, stats)
                        if shutdown == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        elif shutdown == 3:
                            return
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
                    self.operating_system("Cerberus", versions, stats)
                    break

    def shutdown(self, db_filename, game_prog_db, dictionary, notes_dictionary, bagels_prog, ttt_prog, stats):
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file.
        # Exits safely after that.
        while True:
            print("Choose an option.")
            print("1. Sleep")
            print("2. Hibernate")
            print("3. Shutdown")
            print("Type \"info\" for details.")
            shutdown_choice = input()
            if shutdown_choice.lower() in "info":
                print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                      "the shell will result in lost data.")
                print("2. Hibernate\nHibernate saves the current session to disk and exits the python shell. The python shell is closed and all "
                      "data is saved.")
                print("3. Shutdown\nShutdown saves only users and notes to disk. All other data is erased and all apps are quit.")
                input()
                pass
            elif shutdown_choice.lower() in ("sleep", "1"):
                print("Sleeping...")
                return 1

            elif shutdown_choice.lower() in ("hibernate", '2'):
                print("Shutting down...")
                # Aesthetic pause...
                time.sleep(2)
                # Check if any programs are running
                program_running = False
                force_quit = 'shutdown'
                for i in stats:
                    if stats[i] == 'running':
                        print("The " + i + " program is running.")
                        program_running = True
                if program_running:
                    print("Would you like to force quit these apps? Type [ENTER] or [return] to return to the OS to save your progress. "
                          "Type \"shutdown\" to force quit all apps and proceed with shutdown.")
                    force_quit = input()
                else:
                    print("No apps are open.")
                    # Another aesthetic pause...
                    time.sleep(2)
                if force_quit == 'shutdown':
                    print("Shutting down...")
                    # Proceeding with force quitting and shutting down.
                    stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["TicTacToe"] = stats["User Settings"] = \
                        stats["System Info"] = "not running"
                    # First open the databases.
                    db = open(db_filename, 'w')
                    game_prog_db = open(game_prog_db, 'w')
                    # Ready the lists.
                    users = []
                    passwords = []
                    current = []
                    notes = []
                    bagels = []
                    ttt = []
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
                        ttt_user_prog = ''
                        for j in range(8):
                            if ttt_prog[i][0][j] == 'X' or ttt_prog[i][0][j] == 'O':
                                ttt_user_prog += (ttt_prog[i][0][j] + ',')
                            else:
                                ttt_user_prog += ' ,'
                        # Append the last term
                        ttt_user_prog += ttt_prog[i][0][len(ttt_prog[i][0]) - 1] + '.' + ttt_prog[i][1] + '.' + ttt_prog[i][2]
                        # Append user-specific to the list
                        ttt.append(ttt_user_prog)
                        # Now for bagels!
                        # Simple Array, no translation needed.
                        bagels_user_prog = bagels_prog[i][0] + '.' + bagels_prog[i][1] + '.' + bagels_prog[i][2] + '.'\
                                           + bagels_prog[i][3] + '.' + bagels_prog[i][4]
                        pass
                        # After translation and empty notes creation, add everything to the notes list to write to the db later.
                        notes.append(notes_dictionary[i])
                        bagels.append(bagels_user_prog)
                    # Then write each user, password, and current status to the database, saving it to disk.
                    # Also write the notes to the database.
                    for i in range(len(dictionary)):
                        db.write(users[i] + '\t\t' + passwords[i] + '\t\t' + current[i])
                        game_prog_db.write(users[i] + '\t\t' + notes[i] + '\t\t' + bagels[i] + '\t\t' + ttt[i] + '\t\t\n')
                    # Close the databases.
                    db.close()
                    game_prog_db.close()
                    time.sleep(5)
                    print("Shut down complete.")
                    # Fun ride back home!
                    return 3
                else:
                    # Return to allow the user to save their progress.
                    print("Returning to the login screen in 3 seconds.")
                    time.sleep(3)
                    return 0

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
            print("Password set successfully. Entering startup in 3 seconds.")
            time.sleep(3)
            return
        else:
            # If the user did not specify whether or not they wanted a new user.
            self.current_user = 'Guest'
            print("Guest user added. There is no password. Press [ENTER] or [return] during login. Entering startup in 3 seconds.")
            time.sleep(3)
            return
