# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)
from System import operating_system
from System import Loading

Loading.modify_user("Tejas", 7, "running")
Loading.display_user("Tejas")

one = operating_system.boot()
