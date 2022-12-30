# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)
import requests

# thread = Loading.LoadingClass(0)
# thread.thred()

# Loading.modify_user("Tejas", 7, "running")
# Loading.display_user("Tejas")
# print(Loading.caesar_encrypt_hex("Hello"))
# print(Loading.caesar_encrypt_hex(random.choices(Loading.alphabet, k=20)))
# scout_rpg = ScoutRPG.boot('Users\\Tejas')
# sudoku = Sudoku.boot("Users\\Tejas")

try:
    from System import operating_system
    one = operating_system.boot()
except ImportError as e:
    # If any file is missing, code will come here.
    # UPDATE Change whenever the token changes!
    token = "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"
    for sysfile in ("Loading.py", "operating_system.py", "reset.py", "system_recovery.py", "User.py"):
        try:
            file = open("System/" + sysfile, 'x', encoding='utf-8')
            download = requests.get("https://raw.githubusercontent.com/Cerberus1470/Sentiens-Anguis/Tejas/System/{}".format(sysfile),
                                    headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
            file.write(download.content.decode())
            file.close()
        except (FileExistsError, FileNotFoundError):
            pass
    from System import Loading
    Loading.returning("The system is missing files. It will now redownload them from GitHub. Please wait.", 4)
    Loading.progress_bar("Downloading Files", 5)
    Loading.returning("The system has finished downloading/updating files and will now reboot", 5)

