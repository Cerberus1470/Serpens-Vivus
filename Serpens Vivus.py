"""
The main file for any bootup. Very simple, but contains some setup and file protection code.
"""
# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and Tictactoe)

# thread = Loading.LoadingClass(0)
# thread.thread()

# Loading.modify_user("Tejas", 7, "running")
# Loading.display_user("Tejas")
# print(Loading.caesar_encrypt_hex("Hello"))
# print(Loading.caesar_encrypt_hex(random.choices(Loading.ALPHABET, k=20)))
# scout_rpg = ScoutRPG.boot('Users\\Tejas')
# sudoku = Sudoku.boot("Users\\Tejas")
# from System import Registry
# bruh = Registry.Registry("System\\REGISTRY")f
# [print(''.join(i) + '\n', end='') for i in (Loading.upscale("System\\bg\\10x40\\pyidea.bg", 2))]
# from Applications import cabinet
# cabinet.FileEngine.open_file(".\\Users\\Tejas", "sudoku1.sdu")
from System import Loading
Loading.caesar_encrypt("hello", priority=16)

from System import operating_system
one = operating_system.boot(False, True)
