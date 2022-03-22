# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

import operating_system
import os

for subdir, dirs, files in os.walk('Users'):
    for dir1 in dirs:
        try:
            file = open("Users\\%s\\user.info" % dir1, 'r')
            # print(list(file)[0])
            file.close()
        except FileNotFoundError:
            continue

operating_system.boot()
