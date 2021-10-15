import time
from tkinter import *

main_window = Tk()


class OperatingSystem:
    def __init__(self, dictionary, notes, jokes, notepad, bagels, tictactoe, task_manager, user_settings, system_info, reset):
        #Initialize all attributes.
        self.current_user = ''
        self.current_password = ''
        self.jokes = jokes
        self.notepad = notepad
        self.bagels = bagels
        self.tictactoe = tictactoe
        self.taskmgr = task_manager
        self.userset = user_settings
        self.sysinfo = system_info
        self.reset = reset
        #Notes and users
        self.notes = notes
        self.dictionary = dictionary
        #Setting current user and password
        for i in range(len(dictionary)):
            if dictionary[i][2] == 'CURRENT\n':
                self.current_user = dictionary[i][0]
                self.current_password = dictionary[i][1]
                break
        return

    def __repr__(self):
        #Representation of this class.
        return "< This is an OperatingSystem class named " + self.__class__.__name__ + "\n Users: " + str(len(self.dictionary)) + "\n Current User: " + self.current_user + "\n Current Password is hidden. >"

    def operating_system(self, osname, versions, stats):
        #The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
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
            print("Select one from the list above or press [ENTER] or [return] to lock!")
            choice = input()
            #The if elif of choices... so long...
            if choice.lower() in ('jokes', 'joke',  '1'):
                self.jokes.main(stats)
            elif choice.lower() in ('notepad', 'notes', 'note', '2'):
                self.notes[self.current_user] = self.notepad.main(self.notes, stats)
            elif choice.lower() in ('bagels', 'bagels', '3'):
                self.bagels.main()
            elif choice.lower() in ('tictactoe', 'tic-tac-toe', 'ttt', '4'):
                self.tictactoe.main()
            elif choice.lower() in ('task manager', '5'):
                self.taskmgr.main(stats)
            elif choice.lower() in ('user settings', 'usersettings', '6'):
                (self.current_user, self.current_password) = self.userset.main(self.current_user, self.current_password, self.dictionary, stats)
            elif choice.lower() in ('system info', 'sys info', '7'):
                self.sysinfo.main(versions)
            elif choice.lower() in ('reset', '8'):
                self.reset.user_reset(self.current_user)
            elif choice.lower() in ('exit', 'lock computer', '9'):
                print("Computer has been locked.")
                return
            elif choice.lower() in 'debugexit':
                return
            else:
                print("Please choose from the list of applications.")

    def startup(self, versions, stats):
        #The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            print()
            Label(main_window, text="Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.").grid(row=0, column=0)
            print("Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.")
            if self.current_user != 'Guest':
                #Separate while loop for users. Guest users head down.
                while True:
                    print("Enter password.")
                    pwd = input()
                    if pwd == self.current_password:
                        print("Welcome!")
                        self.operating_system("Cerberus", versions, stats)
                        break
                    elif pwd == 'switch':
                        if len(self.dictionary) > 1:
                            (self.current_user, self.current_password) = self.userset.switch_user(self.dictionary, self.current_user, self.current_password, 'os')
                            break
                        else:
                            print("There is currently only one user registered.")
                    elif pwd == 'shutdown':
                        self.shutdown('userpwd_db.txt', self.dictionary, stats)
                        return
                    elif pwd == 'debugexit':
                        return
                    else:
                        print("Sorry, that's the wrong password. Try again.")
            else:
                while True:
                    #The guest account, housed in its own while loop. The only way to exit is to use debugexit.
                    print("The Guest account will boot into the main screen, but any user settings will have no effect. This includes usernames, passwords, game progress, saved notes, etc. Press [ENTER] or [return] to login")
                    if input() == 'debugexit':
                        return
                    self.operating_system("Cerberus", versions, stats)
                    break

    def shutdown(self, db_filename, dictionary, stats):
        #The shutdown method. Saves everything to disk and rides return statements all the way back to the main file.
        # Exits safely after that.
        print("Shutting down...")
        #Check if any programs are running
        program_running = False
        for i in stats:
            if stats[i] == 'running':
                print("The " + i + " program is running.")
                program_running = True
        if program_running:
            print("Would you like to force quit these apps? Type [ENTER] or [return] to return to the OS to save your progress. "
              "Type \"shutdown\" to force quit all apps and proceed with shutdown.")
        forcequit = input()
        if forcequit == 'shutdown':
            #Proceeding with force quitting and shutting down.
            self.reset.reset(stats)
            #First open the database.
            db = open(db_filename, 'w')
            #Ready the lists.
            users = []
            passwords = []
            current = []
            #Append each user, password, and current status to the lists.
            for i in range(len(dictionary)):
                users.append(dictionary[i][0])
                passwords.append(dictionary[i][1])
                current.append(dictionary[i][2])
            #Then write each user, password, and current status to the database, saving it to disk.
            for i in range(len(dictionary)):
                db.write(users[i] + '\t\t' + passwords[i] + '\t\t' + current[i])
            #Close the database.
            db.close()
            time.sleep(5)
            print("Shut down complete.")
            #Fun ride back home!
            return
        else:
            #Return to allow the user to save their progress.
            print("Returning to the login screen in 3 seconds.")
            time.sleep(3)
            return

    def setup(self, dictionary):
        #The setup method. Conveniently sets up the system to run on its first bootup. Modifies the dictionary with a new user.
        print("SETUP: Since this is the first time you're running this OS, you have entered the setup.")
        #Ask the user if they want to make a user or not.
        print("Would you like to create a new user, or login as guest?")
        user_or_guest = input()
        if user_or_guest.lower() in ('new user', 'new', 'user', 'yes'):
            #New user it is!
            print("Name your user:")
            setup_user = input()
            print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
            while True:
                #The while loop handles the password creation. Can only escape under certain circumstances.
                setup_pwd = input()
                if setup_pwd:
                    #If the user entered a password:
                    print("Password set. Enter it again to confirm it.")
                    if setup_pwd == input():
                        break
                    else:
                        #Handle password matching. Loops back to ensure the user typed the correct passwords.
                        print('The passwords you entered didn\'t match. Type the same password twice.')
                else:
                    #If the user did not enter a password:
                    self.current_user = setup_user
                    self.current_password = 'python123'
                    print('Default password set. The password is "python123". Entering startup in 3 seconds.')
                    time.sleep(3)
                    return
            #User entered password correctly twice.
            self.current_user = setup_user
            self.current_password = setup_pwd
            dictionary[0] = self.current_user, self.current_password, 'CURRENT\n'
            print("Password set successfully. Entering startup in 3 seconds.")
            time.sleep(3)
            return
        else:
            #If the user did not specify whether or not they wanted a new user.
            self.current_user = 'Guest'
            print("Guest user added. There is no password. Press [ENTER] or [return] during login. Entering startup in 3 seconds.")
            time.sleep(3)
            return
