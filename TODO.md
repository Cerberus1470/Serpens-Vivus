KEY:
! means important.
~ means in progress.
^ means completed.
X means rejected.

# TODO - Basic
    ^ ! - Loops in user settings (delete more than one user)
    ^ - Edit username and password
    ^ - User-specific notes and game progress
    ^ ! - Merge shutdown and hibernate (since they share a lot of root code)
    ^ - Fix imports
    ^ ! - Add shutdown, hibernate, and sleep options on shutdown menu
    ^ - Add user-specific app status (app sessions)
    ^ - Change status dictionary
    ^ - Change current user status to boolean
    ^ ! - Fix add user with game progress
    ^ ! - Fix restarting!
    ^ - Delete all aesthetic pauses in shutdown function
    ^ - Do loading animation for all aesthetic pauses in all files!!!!

# TODO - Advanced
    ^ ! - Add admins and standard users.
    ^ - Request password before deleting user (then remove the check for admin users)
    ^ - Add 3 recently deleted users
        ^ - Add log of who deleted who
    ^ - Event Log
        ^ - Basically keeps track of every event that happens in the computer.
        ^ - It will also be accessible using an app: Event Viewer
            ^ - Event Viewer will basically show chunks of events based on time.
                ^ - This chunk is calculated if the gap between logged events is greater than 10 minutes.
            ^ - There will be a reset function in the app as well.
    ^ ! - Rewrite Shutdown function entirely
        ^ - Explicitly write conditions for all shutdown methods
    ^ - Add a lockout for _ number of incorrect passwords.
    ^ - Add speed up or slow down to program
    ^ ! - Comprehensive app screen
        ^ - Categories! Apps, utilities, games, power
        ^ - Admin specific apps, standard users cannot see them
    ^ ! - Rework startup method completely
    ^ - Add parent-child hierarchy
    ^ X ! - Encrypt typed password - REJECTED. This turned out to be a LOT harder than I thought. I seriously have no idea how this works.
        - Just had to use a different library to make it work in IDE and in terminal.
    ^ - Rework Cerberus.py into operating_system.py
        I just figured out that restart actually does nothing! It's supposed to shut down the OS and read from disk storage again from scratch... But it doesn't...
        New function: boot. Boot will read everything from disk storage. Basically what goes on in Cerberus.py now goes
        into a function in operating_system. The goal is to just have the while loop and public variables in Cerberus.py
        ^ ! - Fix Guest User!
        ^ ! - Fix Reset
        ^ - Move reading code into boot function!
        ^ - Encrypt db_protected.txt using Fernet or Caesar Cypher
    ^ - Calendar app???
    ^ ! - Savable user-specific games, similar to notepad. Every game gets the treatment!
    - Add debug mode. Documentation Below.
    ^ - Add Sonar.
    ^ - Fix Guest functionality for all apps
        X - Add a guest subroutine that doesn't ask for filenames, just makes a new game when launching, no file selection, etc.
        ^ - Just handle the FileNotFound error and tell the user that the message will show up.
    ^ - Implement recovery password
    ^ - Change Saved State to Booleans
    ^ - Change number of program statuses to reflect how many applications are there, in operating_system.reload().
    X - Create error to upgrade user info files to reflect how many applications there are. - REJECTED after the Saved_State Update.
    ^ - Handle application errors.
        ^ - This will be separate from system crashes (BSOD), and will basically boot you back to the home screen.
    - Mid-method home button action and saved_state restoring.
    ^ - Lock "button". This will do the same as the home button, but taken back to the lock screen.
    - Revamp Setup to ask which apps to download. This will go well with the game store idea.
    - Built-in Python Console
    - Spreadsheet app???

# TODO - Really advanced
    ~ - Add user personalization. See documentation below.
    - Add a game store. I'll add some documentation below.
    ^ ~ - Implement hashing (encrypting the databases)
        ^ - Error Correction in databases.
        ^ - Develop error correcting app after implementing encryption. More documentation below.
    ~ - Implement Threads
    ^ ~ - Revamp db_unprotected.txt into user directories. More documentation below.
        ^ ~ - Completely revamp Notes app. See below for documentation.
            - Add editing functionality.
    ~ - Make the saved_state actually do something (and revamp task manager with it)
    ~ - Revamp Guest user!
        ^ - Make guest user more user-friendly. Remove "Games will say the path is invalid", make a workaround!
            ^ - Add guest folder, and ask user if they want to save data to a new user
        ^ - Add guest user at startup.
    ^ - Registry Editor! And registry keys. Documentation Below.

# TODO - POCS4.0 after gamma01:
    ^ - Guest user folder
    ^ - Fix game engine
    ^ - Develop registry disk methods
    ^ - Fully integrate registry into OS
    ^ - Finish Settings App
    ^ - Rework System Recovery
    ^ - GitHub Downloads
    ^ - Update Bug Trackers
    ^ - Phase out unneeded apps (reset)
    ^ - Finish creating backgrounds
    ^ - In-built Python console
    ^ - File Explorer
    - Merge with master!
    - In case I forget, mid-method saved_state is possible by saving each user input to a list, saved with each application.
      When the saved_state object is restored, the list will be checked. If there are items, they will be iterated and typed
      with pynput.keyboard.Controller().type() so that each input() can be filled with the respective inputs from the user
      and the state can be restored.

## Administrators:
- Admins have elevated access that allow for certain functions. These include:
    - Creating new Users
    - Managing Users
        - Deleting
        - Editing other user info (not current user info)
    - Resetting the OS
    - Installing games (future)
    - Debug mode

## Debug Mode:
Finally, let's write the documentation. This has been an idea too long.
- Basically shows a bunch of debug info, like:
    - System versions
    - User inputs
    - Code line number
    - Any exception
        - The opportunity to go back to the line of code, etc.

## Game store:
- This is a collection of games that the user can install.
- Saving game progress will no longer be hardcoded with this addition.
X Each game will be iterated through and the individual user progress will be written to the database.
    X - Each game will now have game files, so no more saving through shutdown.
- Each game will also be completely internalized. Every parameter given to __init__ and boot are literals, no objects.
X - This is going to be really hard.
- ACTUALLY, Since every game is isolated and doesn't require anything, doing this is much easier.

## Hashing:
- Essentially encrypting the databases.
- This will prevent tampering with the saved data.
X - Error correction (SCRAPPED):
    X - If the data becomes corrupted from an unexpected shutdown or something, an error correcting app will be launched on the next startup.
    X - The user will also be able to launch this if they believe the OS is corrupt.
    X - This will do 2 things: Error check the encrypted databases, and error check the entire root code. Think Disk Check or Recovery Tools for Windows.
    X - The function call will replace the corruption error message being displayed during startup with corrupted databases.
    X - This will probably be even harder than the Game store.
- New Error correction:
    - Essentially, this will provide a comprehensive error report of what happened, possible causes, and how to fix it.

## New user directories:
- Each user will get their own dedicated directory.
- Upon deletion or username edits, the user directory will be changed as well.
- This directory will now store whatever was in db_unprotected.txt. This includes game progress.
- Each game will be in its own notepad file.
    - New Notepad:
        - Basically, the user can create txt files at will, in their own directory.
        - The files will be read from storage into memory, and will be editable and savable.
        - Saving txt files will be completely different from shutdown.

## User Personalization:
- Users can change the color of the background, the color of the text, perhaps even the language????
- Completely new app.
- Could spark the change from separate settings apps to a central Settings app!

## Registry Editor:
- Module, Class, and App to change global system/app settings.
- This combined with the game store with a fool-proof iteration protocol that will allow users to create their own apps, add to the registry, and use those registry entries!
- In the registry class, there will be a method to modify the registry.
    - Security risks will also be handled. Elevation will be considered and some kind of password will be required to make sure no one can make a game with registry-altering code.
- Before the module is created, I'll put it in Loading.

## New Home Screen Ideas (default wallpaper)
 -  Taskbar style:
```
     ________________         _____
    |  _|            |     __|_o__ |
    |_| -.- -.-      |    |   _____| __
    |   -'- -'       |    |__| _____|  |
    |                |        | _______|
    |   ___          |        |__o_|
    |________________|
    SV | Bagels  Hangman  Settings  Sudoku

    Serpens Vivus - Apps
    Bagels          ScoutRPG        System Info
    Event Viewer    Settings        Task Manager
    Hangman         Sonar           TicTacToe
    Jokes           SpeedSlow
    Notepad         Sudoku

    Serpens Vivus - Apps
    UTILITIES       GAMES
    Event Viewer    Bagels      Sudoku
    Notepad         Hangman     TicTacToe
    Settings        Jokes
    SpeedSlow       ScoutRPG
    System Info     Sonar
```
    - Amount of space adjusted for how many apps shown.
    - Apps screen can be alphabetical or categorized.
    - Taskbar space is also decided by resolution.

- Classic Style:
    APPLICATIONS
    UTILITIES               GAMES                   ADMIN
    Settings                Bagels                  Reset
    System Info             Tictactoe               Event Viewer
    Notepad                 Hangman                 Task Manager
    SpeedSlow               Sonar
                            Joke Teller
                            ScoutRPG

## Calendar App:
 <      2024      ^
<< <   January  ^ ^^
S  M  T  W  T  F  S
1  2  3  4  5  6  7
8  9  10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31

- Year arrows keep the month, update the days
- Month single arrow is one-by-one, don't forget rollover
- Month double arrows are beginning and end of the current year. Disable when already at beg/end
- Travel to Date/Month/Year feature! Default Month and Date to 1 if not specified
- Logic net for input text. Y<, Y^, M<, M^, M<<, M^^, etc.