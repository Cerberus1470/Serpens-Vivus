import time


class UserSettings:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a UserSettings class named " + self.__class__.__name__ + ">"

    def add_user(self, dictionary):
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

    def delete_user(self, dictionary, current_user):
        print("Choose a user to delete or type 'exit' to exit.")
        pos = ''
        count = 1
        for i in dictionary:
            print(str(count) + '. ' + i)
            count += 1
        while True:
            delete_sel = input()
            if delete_sel == 'exit':
                return
            elif delete_sel in dictionary:
                for i in dictionary:
                    if delete_sel == i:
                        if delete_sel == current_user:
                            print("You can't delete the current user! Login with a different user to delete this one.")
                            print("Returning to the User Settings in 3 seconds.")
                            time.sleep(3)
                            return
                        else:
                            pos = i
                try:
                    deleted_user = dictionary.pop(pos)
                    print("User deleted successfully. Returning to the User Settings in 3 seconds.")
                    time.sleep(3)
                    return
                except KeyError:
                    pass

            else:
                print("Please choose a user from the list or type \"exit\" to exit.")

    def switch_user(self, dictionary, current_user, current_password, src):
        print("Current User: " + current_user)
        print("Choose a user.")
        count = 1
        for i in dictionary:
            print(str(count) + '. ' + i)
            count += 1
        while True:
            user_selection = input()
            pos = 0
            isindb = False
            for i in dictionary:
                isindb = isindb or user_selection == i
            if user_selection.lower() == 'exit':
                break
                # Checking if the user selection is in the user pwd database.
            elif isindb:
                for i in dictionary:
                    if user_selection == i:
                        dictionary[i] = (dictionary[i][0], 'CURRENT\n')
                        pos = i
                    if current_user == i:
                        dictionary[i] = (dictionary[i][0], '\n')
                current_user = pos
                current_password = dictionary[pos][0]
                break
            else:
                print("Choose a user from the list or type 'exit' to exit.")
        if src == 'os':
            print("Returning to the login screen in 3 seconds.")
        else:
            print("Returning to the User Settings in 3 seconds.")
        time.sleep(3)
        return current_user, current_password

    def main(self, current_user, current_password, dictionary, stats):
        stats["userset"] = "running"
        print("Welcome to User Settings!")
        print("Here you can edit the username and password of the current user!")

        while True:
            print("Current User: " + current_user)
            print("1. Edit Username")
            print("2. Edit Password")
            print("3. Add new User")
            print("4. Delete User")
            print("5. Switch User")
            print("\nChoose an option or press [ENTER] or [return] to return to the applications screen!")
            setchoice = input()
            if setchoice.lower() in ('edit username', 'edit uname', '1'):
                print("New Username:")
                # new_uname = input()
                # for i in user_pwd_database:
                #     (user, pwd, current) = i.split('\t\t', 2)
                #     if current_user == user:
                #         result_database.write(new_uname + '\t\t' + current_password + '\t\t' + current + '\n')
                #     else:
                #         result_database.write(user + '\t\t' + pwd + '\t\t' + current + '\n')
                #     current_user = new_uname
                # user_pwd_database.close()
                # result_database.close()
                # del user_pwd_database, result_database
                # os.replace('resultfile.txt', db_filename)
                # print("New Username successfully set!")
            elif setchoice.lower() in ('edit password', 'edit pwd', '2'):
                print("Old Password:")
                old_pwd = input()
                if old_pwd == current_password:
                    print("New Password:")
                    new_pwd = input()
                    current_password = new_pwd
                    print("New Password successfully set!")
                else:
                    print("The password is incorrect.")
            elif setchoice.lower() in ('add new user', '3'):
                self.add_user(dictionary)
            elif setchoice.lower() in ('delete user', '4'):
                self.delete_user(dictionary, current_user)
            elif setchoice.lower() in ('switch user', '5'):
                (current_user, current_password) = self.switch_user(dictionary, current_user, current_password, 'main')
            else:
                return current_user, current_password
