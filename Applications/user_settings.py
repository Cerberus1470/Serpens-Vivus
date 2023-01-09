"""
Module user_settings. Contains the application and pertinent classes.
"""
from System import Loading
import os


def returning():
    """
    Widely used function to display that the system is returning to the main menu.
    :return: Nothing.
    """
    Loading.returning("Returning to User Settings...", 2)


class UserSettings:
    """
    Class UserSettings. Contains all the functions and application info.
    """
    category = "utilities"

    @staticmethod
    def boot(os_object):
        """
        Method to regulate startup of the application.
        :param os_object: The OS object with all its info.
        :return: "regular".
        """
        # os_object.current_user.saved_state["User Settings"] = "running"
        if UserSettings.main(UserSettings(), os_object) == 1:
            return 'regular'

    def __init__(self):
        return

    def __repr__(self):
        return "< This is a UserSettings class named " + self.__class__.__name__ + ">"

    def main(self, os_object):
        """
        The main application screen.
        :param os_object: The OS object to get info from.
        :return: 1 if the user was switched, Nothing otherwise.
        """
        print("Welcome to User Settings!")
        print("Here you can edit the username and password of the current user!")

        while True:
            print("\nCurrent User: " + os_object.current_user.username)
            print("\nOther users:")
            for i in os_object.users:
                if i.username != os_object.current_user.username:
                    print(str(os_object.users.index(i) + 1) + ": " + i.username)
            print("\n1. Edit Username")
            print("2. Edit Password")
            print("3. Add new User")
            print("4. Delete User")
            print("5. Restore User")
            print("6. Switch User")
            print("\nChoose an option or press [ENTER] or [return] to return to the applications screen!")
            choice = Loading.pocs_input(message="")
            if choice == '':
                return
            if choice.lower() in ('edit username', 'edit uname', '1'):
                self.edit_uname(os_object)
            elif choice.lower() in ('edit password', 'edit pwd', '2'):
                self.edit_pwd(os_object)
            elif choice.lower() in ('add new user', '3', 'add',  'new', 'new user', 'add user', 'add new'):
                self.add_user(os_object)
            elif choice.lower() in ('delete user', '4', 'delete'):
                self.delete_user(os_object)
            elif choice.lower() in ('restore user', '5', 'restore'):
                self.restore_user(os_object)
            elif choice.lower() in ('switch user', '6', 'switch'):
                self.switch_user(os_object)
                return 1
            else:
                Loading.returning("Please choose from the list of options.", 2)

    @staticmethod
    def print_all_users(message, users):
        """
        Widely-used method that prints all users and collects an input.
        :param message: Message to display first.
        :param users: The list of users.
        :return: The selected user if the selection was valid, Nothing otherwise.
        """
        print(message)
        for i in users:
            print(str(users.index(i) + 1) + ": " + i.username)
        user = input()
        for i in users:
            if user == i.username:
                return i
        Loading.returning("Sorry, the username was not in the list.", 2)
        return

    def edit_uname(self, os_object):
        """
        The sub-program to edit the username of a selected user.
        Defaults to changing the current_user, but if the current user is an Admin, allows you to choose whose username to change.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        user = os_object.current_user
        if os_object.current_user.elevated:
            user = self.print_all_users("Choose the user whose username you want to edit", os_object.users)
        if user:
            print("New Username for " + user.username + ":")
            new_uname = input()
            if new_uname == "Default" or new_uname in [i.username for i in os_object.users]:
                Loading.returning("That username is taken.", 3)
            else:
                # Find the current user (or the specified user) and change their name to the new name.
                if Loading.modify_user(user.username, 1, new_uname) == 1:
                    os_object.users[os_object.index([i for i in os_object.users if i == user])].username = new_uname
                    Loading.returning("New Username successfully set!", 2)

    def edit_pwd(self, os_object):
        """
        The sub-program to edit the password of a selected user.
        Defaults to changing the current_user, but if the current user is an Admin, allows you to choose whose password to change.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        user = os_object.current_user
        if os_object.current_user.elevated:
            user = self.print_all_users("Choose the user whose password you want to edit.", os_object.users)
        if user:
            print("Old Password for " + user.username + ":")
            old_pwd = input()
            if old_pwd == user.password:
                new_pwd = input("New Password:")
                if new_pwd == input("Enter the new password again:"):
                    if Loading.modify_user(user.username, 2, new_pwd) == 1:
                        Loading.returning("New Password successfully set!", 2)
                    else:
                        Loading.returning("An error occurred. Please reboot the system safely.", 2)
                else:
                    Loading.returning("The passwords did not match.", 2)
            else:
                Loading.returning("The password is incorrect.", 3)
            return

    @staticmethod
    def add_user(os_object):
        """
        Sub-program to add a new user to the OS. Requires Elevation.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        from System import User
        # Adding a new user!
        if not os_object.current_user.elevated:
            print("You do not have sufficient privileges to add users.")
            returning()
            return
        print("Welcome to the Add User setup wizard!")
        while True:
            print('Would you like this user to be a Standard User or an Administrator?\nType "info" for descriptions, or "exit" to leave.')
            user_type = input()
            if user_type == "info":
                print("1. Standard Users can perform simple system tasks and have access to all utilities and games."
                      "\n2. Administrators can perform simple and complex system tasks and have access to utilities, games, and administrative tools.\n")
            elif user_type.lower() in ("standard", "standard user", "regular", "normal"):
                user_type = "StandardUser"
                break
            elif user_type.lower() in ("administrator", "admin", "elevated", "bruh"):
                user_type = "Administrator"
                break
            elif user_type.lower() == "exit":
                return
            else:
                print("Please type a valid response.")
        # Take a name
        while True:
            add_user = input("Name your user:\n")
            for i in os_object.users:
                if add_user == i.username or add_user == "Default":
                    Loading.returning("That username is taken")
                    break
            else:
                break
        print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
        # While loop for the password.
        while True:
            # Ask for password
            add_pwd = input()
            # If password entered:
            if add_pwd:
                # Make sure it's the same password
                if add_pwd == input("Password set. Enter it again to confirm it.\n"):
                    break
                else:
                    print("The passwords you entered didn't match. Type the same password twice.")
            else:
                # Default password
                add_pwd = 'python123'
                print('Default password set. The password is "python123".')
                break
        # Add this to the user dictionary
        if user_type == 'StandardUser':
            os_object.users.append(User.StandardUser(add_user, add_pwd, False))
        else:
            os_object.users.append(User.Administrator(add_user, add_pwd, False))
        os.mkdir('Users\\%s' % add_user)
        file = open('Users\\%s\\info.usr' % add_user, 'w')
        file.write(Loading.caesar_encrypt(user_type + '\t\t' + add_user + '\t\t' + add_pwd + "\t\t" + "False" + '\t\t') + '\n\n')
        file.close()
        print("Password set successfully.")
        Loading.returning("New user has been added. Returning to the User Settings in 3 seconds.", 3)
        return

    def delete_user(self, os_object):
        """
        Sub-program to delete users.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        if not os_object.current_user.elevated:
            print("You do not have sufficient privileges to delete users.")
            returning()
            return
        while True:
            delete_sel = self.print_all_users("Choose a user to delete or type 'exit' to exit.", os_object.users)
            if delete_sel:
                for i in os_object.users:
                    if delete_sel == i:
                        if input('Are you sure? Type "YES" if you are sure.\n') == 'YES':
                            if i.current:
                                Loading.returning("You can't delete the current user! Login with a different user to delete this one.", 3)
                                break
                            else:
                                Loading.log("The user {} was deleted by {}".format(i.username, os_object.current_user.username))
                                os_object.recently_deleted_users.append(os_object.users.pop(os_object.users.index(i)))
                                for subdir, dirs, files in os.walk("Users"):
                                    if subdir == "Users\\" + delete_sel.username:
                                        try:
                                            for j in files:
                                                os.remove(subdir + '\\' + j)
                                            os.rmdir(subdir)
                                        except OSError:
                                            pass
                                Loading.returning("Deleting user... ", 3)
                                print("\nUser deleted successfully.")
                                break
                        else:
                            print("Incorrect password.")
                            pass
            print("\nDelete another user? Yes or no?")
            if input() == 'yes':
                pass
            else:
                returning()
                return

    @staticmethod
    def restore_user(os_object):
        """
        Sub-program to restore a recently deleted user. This list clears with every reboot.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        if not os_object.current_user.elevated:
            print("You do not have sufficient privileges to restore users.")
            returning()
            return
        if os_object.recently_deleted_users:
            print("Here is a list of the recently deleted users.")
            for i in range(len(os_object.recently_deleted_users)):
                print(str(i+1) + ". " + os_object.recently_deleted_users[i].username)
            restore = input("Type the name of the user you want to restore.\n")
            is_in_db = False
            for i in os_object.recently_deleted_users:
                if restore == i.username:
                    os_object.users.append(i)
                    os_object.recently_deleted_users.pop(os_object.recently_deleted_users.index(i))
                    is_in_db = True
                    print("The user was successfully restored.")
                    Loading.log("The user {} was deleted by {}.".format(i.username, os_object.current_user.username))
                    returning()
            if not is_in_db:
                Loading.returning("The user specified is not in the list of recently deleted users. Returning to User Settings.", 3)
        else:
            print("There are no recently deleted users available.", 3)
            returning()
            return

    @staticmethod
    def switch_user(os_object):
        """
        Sub-program to switch the current user.
        :param os_object: The OS Object to get info from.
        :return: Nothing.
        """
        if len(os_object.users) > 1:
            print("Current User: " + os_object.current_user.username)
            for i in os_object.users:
                print(str(os_object.users.index(i) + 1) + ": " + i.username)
            while True:
                user_selection = input("Choose a user.\n")
                is_in_db = False
                for i in os_object.users:
                    is_in_db = is_in_db or user_selection == i.username
                if user_selection.lower() == 'exit':
                    break
                # Checking if the user selection is in the user pwd database.
                elif is_in_db:
                    for i in os_object.users:
                        if user_selection == i.username:
                            i.current = True
                            os_object.current_user.current = False
                            os_object.current_user = i
                    break
                else:
                    print("Choose a user from the list or type 'exit' to exit.")
        else:
            print("There is only one user registered.")
            return
        Loading.returning("Returning to the login screen in 3 seconds.", 3)
