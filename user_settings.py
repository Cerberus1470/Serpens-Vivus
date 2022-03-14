import time
import Loading


class UserSettings:
    def __init__(self):
        self.recently_deleted_users = []
        return

    def __repr__(self):
        return "< This is a UserSettings class named " + self.__class__.__name__ + ">"

    @staticmethod
    def edit_uname(os_object):
        user = os_object.current_user.username
        user_present = ""
        if os_object.current_user.elevated:
            print("Choose the user whose username you want to edit.")
            for i in os_object.users:
                print(str(os_object.users.index(i) + 1) + ": " + i.username)
            user = input()
            for i in os_object.users:
                if user == i.username:
                    user_present = "yay"
            if not user_present:
                print("Sorry, the username was not in the list.")
                return
        print("New Username for " + user + ":")
        new_uname = input()
        # Find the current user (or the specified user) and change their name to the new name.
        for i in os_object.users:
            if i.username == user:
                i.username = new_uname
                print("New Username successfully set!")
                time.sleep(2)
                return

    @staticmethod
    def edit_pwd(os_object):
        user = os_object.current_user
        user_present = ""
        if os_object.current_user.elevated:
            print("Choose the user whose password you want to edit.")
            for i in os_object.users:
                print(str(os_object.users.index(i) + 1) + ": " + i.username)
            user = input()
            for i in os_object.users:
                if user == i.username:
                    user_present = "yay"
                    user = i
            if not user_present:
                print("Sorry, the username was not in the list.")
                return
        print("Old Password for " + user.username + ":")
        old_pwd = input()
        if old_pwd == user.password:
            print("New Password:")
            new_pwd = input()
            print("Enter the new password again:")
            if new_pwd == input():
                user.password = new_pwd
                print("New Password successfully set!")
                time.sleep(2)
                pass
            else:
                print("The passwords did not match.")
                time.sleep(2)
                pass
            pass
        else:
            print("The password is incorrect.")
            pass
        return

    @staticmethod
    def add_user(os_object):
        # Adding a new user!
        if not os_object.current_user.elevated:
            print("You do not have sufficient privileges to delete users.")
            return
        print("Welcome to the Add User setup wizard!")
        print('You are an administrator!\n')
        while True:
            print('Would you like this user to be a Standard User or an Administrator?\nType "info" for descriptions, or "exit" to leave.')
            user_type = input()
            if user_type == "info":
                print("1. Standard Users have limited privileges. More description coming soon.")
                print("2. Administrators can do anything.")
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
        add_user = input("Name your user:\n")
        print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
        # While loop for the password.
        while True:
            # Ask for password
            add_pwd = input()
            # If password entered:
            if add_pwd:
                print("Password set. Enter it again to confirm it.")
                # Make sure it's the same password
                if add_pwd == input():
                    break
                else:
                    print("The passwords you entered didn't match. Type the same password twice.")
            else:
                # Default password
                # Add this to the user dictionary
                os_object.users.append(globals()[user_type](add_user, "python123", False, ""))
                Loading.returning('Default password set. The password is "python123". Returning to the User Settings in 3 seconds.', 3)
                # Return from here itself, don't run the following.
                return
        # Add this to the user dictionary
        os_object.users.append(globals()[user_type](add_user, add_pwd, False, ""))
        Loading.returning("Password set successfully. Returning to the User Settings in 3 seconds.", 3)
        return

    def delete_user(self, os_object):
        if not os_object.current_user.elevated:
            print("You do not have sufficient privileges to delete users.")
            return
        while True:
            print("Choose a user to delete or type 'exit' to exit.")
            for i in os_object.users:
                print(str(os_object.users.index(i) + 1) + ": " + i.username)
            delete_sel = input()
            if delete_sel == 'exit':
                return
            is_in_db = False
            for i in os_object.users:
                is_in_db = is_in_db or delete_sel == i.username
            if is_in_db:
                for i in os_object.users:
                    if delete_sel == i.username:
                        if input('Are you sure? Type "YES" if you are sure.\n') == 'YES':
                            if i.current:
                                print("You can't delete the current user! Login with a different user to delete this one.")
                                time.sleep(3)
                                break
                            else:
                                try:
                                    self.recently_deleted_users.append(os_object.users.pop(os_object.users.index(i)))
                                    Loading.returning("Deleting user... ", 3)
                                    break
                                except KeyError:
                                    pass
                        else:
                            print("Incorrect password.")
                            break
                print("\nUser deleted successfully.\nDelete another user? Yes or no?")
                if input() == 'yes':
                    pass
                else:
                    Loading.returning("Returning to the User Settings in 2 seconds.", 2)
                    return
            else:
                print("Please choose a user from the list or type \"exit\" to exit.")
                pass

    def restore_user(self, os_object):
        if self.recently_deleted_users:
            print("Here is a list of the recently deleted users.")
            for i in range(len(self.recently_deleted_users)):
                print(str(i+1) + ". " + self.recently_deleted_users[i].username)
            restore = input("Type the name of the user you want to restore.\n")
            is_in_db = False
            for i in self.recently_deleted_users:
                if restore == i.username:
                    os_object.users.append(i)
                    self.recently_deleted_users.pop(self.recently_deleted_users.index(i))
                    is_in_db = True
            if not is_in_db:
                Loading.returning("The user specified is not in the list of recently deleted users. Returning to User Settings.", 3)
        else:
            Loading.returning("There are no recently deleted users available. Returning to User Settings.", 3)
            return

    @staticmethod
    def switch_user(os_object, src):
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
        if src == "os":
            Loading.returning("Returning to the login screen in 3 seconds.", 3)
        else:
            Loading.returning("Returning to the user settings screen in 3 seconds.", 3)
        return

    def main(self, os_object):
        print("Welcome to User Settings!")
        print("Here you can edit the username and password of the current user!")

        while True:
            print("Current User: " + os_object.current_user.username)
            print("\nOther users:")
            for i in os_object.users:
                print(str(os_object.users.index(i) + 1) + ": " + i.username)
            print("\n1. Edit Username")
            print("2. Edit Password")
            print("3. Add new User")
            print("4. Delete User")
            print("5. Restore User")
            print("6. Switch User")
            print("\nChoose an option or press [ENTER] or [return] to return to the applications screen!")
            choice = input()
            if choice.lower() in ('edit username', 'edit uname', '1'):
                self.edit_uname(os_object)
            elif choice.lower() in ('edit password', 'edit pwd', '2'):
                self.edit_pwd(os_object)
            elif choice.lower() in ('add new user', '3'):
                self.add_user(os_object)
            elif choice.lower() in ('delete user', '4'):
                self.delete_user(os_object)
            elif choice.lower() in ('restore user', '5'):
                self.restore_user(os_object)
            elif choice.lower() in ('switch user', '6'):
                self.switch_user(os_object, 'user_set')
            else:
                return
