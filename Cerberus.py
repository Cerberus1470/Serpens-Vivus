# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

from operating_system import OperatingSystem

protected_db_name = 'db_protected.txt'
unprotected_db_name = 'db_unprotected.txt'
running = True
corrupt_message = "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nTHE DATABASE IS CORRUPTED. PLEASE CHECK THE MANUAL, QUIT THE OS, AND RECONFIGURE THE DATABASE." \
                  "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nCorrupted Database: %s\nCorrupted Section: %s\n"

# results = [0]
#
# example = Loading.Loading(results)

while running:
    # Initializing operating system with __init__
    Cerberus = OperatingSystem(protected_db_name, unprotected_db_name, corrupt_message)
    if len(Cerberus.users) <= 0:
        Cerberus.setup()
    if Cerberus.startup() == 4:
        pass
    else:
        running = False

# print(results[0])
