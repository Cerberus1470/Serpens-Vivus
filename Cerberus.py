# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)
import os
from System import operating_system

# sys.path.append('Applications')

# Loading.progress_bar("Loading...", 5)

for subdir, dirs, files in os.walk('Users'):
    for dir1 in dirs:
        try:
            info = open("Users\\%s\\info.usr" % dir1, 'a')
            # print(dir1[len(dir1)-3:len(dir1)])
            # print(list(file)[0])
            info.close()
        except FileNotFoundError:
            continue
    for file in files:
        try:
            if file[len(file)-3:len(file)] == 'ttt':
                # print(str(files.index(file)) + '. ' + file)
                pass
        except FileNotFoundError:
            continue

operating_system.boot()
