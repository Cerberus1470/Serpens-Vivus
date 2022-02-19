import time


class UserSettings:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a UserSettings class named " + self.__class__.__name__ + ">"

    @staticmethod
    def add_user(os_object):
        # Adding a new user!
        print("Welcome to the Add User setup wizard!")
        print("Name your user:")
        # Take a name
        add_user = input()
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
                    print('The passwords you entered didn\'t match. Type the same password twice.')
            else:
                # Default password
                add_password = 'python123'
                # Add this to the user dictionary
                dictionary[add_user] = (add_password, '\n')
                print('Default password set. The password is "python123". Returning to the User Settings in 3 seconds.')
                time.sleep(3)
                # Return from here itself, don't run the following.
                return
        add_password = add_pwd
        # Add this to the user dictionary
        dictionary[add_user] = (add_password, '\n')
        print("Password set successfully. Returning to the User Settings in 3 seconds.")
        time.sleep(3)
        return

    @staticmethod
    def delete_user(os_object):
        while True:
            print("Choose a user to delete or type 'exit' to exit.")
            pos = ''
            count = 1
            for i in dictionary:
                print(str(count) + '. ' + i)
                count += 1
            flag = True
            while flag:
                delete_sel = input()
                if delete_sel == 'exit':
                    return
                elif delete_sel in dictionary:
                    for i in dictionary:
                        if delete_sel == i:
                            print("Enter the password for " + i)
                            if input() == dictionary[i][0]:
                                if delete_sel == current_user:
                                    print("You can't delete the current user! Login with a different user to delete this one.")
                                    time.sleep(3)
                                    flag = False
                                    break
                                else:
                                    pos = i
                                    pass
                            else:
                                print("Incorrect password.")
                                break
                    try:
                        deleted_user = dictionary.pop(pos)
                        print("User deleted successfully. Returning to the User Settings in 3 seconds.")
                        time.sleep(3)
                        return
                    except KeyError:
                        pass
                else:
                    print("Please choose a user from the list or type \"exit\" to exit.")
                    pass
                pass
            print("Delete another user? Yes or no?")
            if input() == 'yes':
                pass
            else:
                print("Returning to the User Settings in 3 seconds.")
                return

    @staticmethod
    def switch_user(os_object, src):
        print("Current User: " + os_object.current_user.username)
        print("Choose a user.")
        for i in os_object.users:
            print(str(os_object.users.index(i)) + ": " + i.username)
        while True:
            user_selection = input()
            is_in_db = False
            for i in os_object.users:
                is_in_db = is_in_db or user_selection == i.username
            if user_selection.lower() == 'exit':
                break
            # Checking if the user selection is in the user pwd database.
            elif is_in_db:
                for i in os_object.users:
                    if user_selection == i.username:
                        i.current = "CURRENT"
                        os_object.current_user.current = ""
                        os_object.current_user = i
                break
            else:
                print("Choose a user from the list or type 'exit' to exit.")
        print("Returning to the login screen in 3 seconds.")
        time.sleep(3)
        if src == "os":
            return 0
        else:
            return 1

    def main(self, os_object):
        print("Welcome to User Settings!")
        print("Here you can edit the username and password of the current user!")

        while True:
            print("Current User: " + os_object.current_user.username)
            print("1. Edit Username")
            print("2. Edit Password")
            print("3. Add new User")
            print("4. Delete User")
            print("5. Switch User")
            print("\nChoose an option or press [ENTER] or [return] to return to the applications screen!")
            choice = input()
            if choice.lower() in ('edit username', 'edit uname', '1'):
                print("New Username for " + os_object.current_user.username + ":")
                new_uname = input()
                #Find the current user and change their name to the new name.
                for i in os_object.users:
                    if i.current == "CURRENT":
                        i.username = new_uname
                        break
                print("New Username successfully set!")
                time.sleep(2)
            elif choice.lower() in ('edit password', 'edit pwd', '2'):
                print("Old Password:")
                old_pwd = input()
                if old_pwd == os_object.current_user.password:
                    print("New Password:")
                    new_pwd = input()
                    print("Enter the new password again:")
                    if new_pwd == input():
                        #Find the current user and change their password to the new password.
                        for i in os_object.users:
                            if i.current == "CURRENT":
                                i.password = new_pwd
                                break
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
            elif choice.lower() in ('add new user', '3'):
                self.add_user(os_object)
            elif choice.lower() in ('delete user', '4'):
                self.delete_user(os_object)
            elif choice.lower() in ('switch user', '5'):
                self.switch_user(os_object, 'main')
            else:
                return
