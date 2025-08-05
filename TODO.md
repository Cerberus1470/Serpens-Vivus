KEY:\
! means important.\
~ means in progress.\
^ means completed.\
X means rejected.

# TODO - Basic
- Optimize elevation (method or something) to remove the elevated attribute from users
- Taskbar settings: streamline adding, removing, add from open app (super key)
- Add elevation for all admin apps.

# TODO - Advanced
- Add debug mode. Documentation Below.
- Mid-method home button action and saved_state restoring.
- Revamp Setup to ask which apps to download. This will go well with the game store idea.
- ~ Built-in Python Console
- Spreadsheet app???
- ~ Create Manifest app for the Registry
  - Add SAFE verification before reloading! Don't just bring up the error instantly, offer a flashback.
  - Fix adding keys with paths. The loading alphabet doesn't have \ in it, so adding a key with any path breaks.
- Add elevation for admin apps (at the os level)
- ~ Open apps from Cabinet
- Create Companion app as a tutorial app.
  - Add help msgs for all applications, copy-paste their help msgs into Companion.
  - Chapters will be System (sub-chapters are OS, Recovery, and Registry apps), then all Applications, iteratively. Use attributes, don't hard-code.
- Create Search and Rescue app for System Recovery.

# TODO - Really advanced
- ^ Add user personalization. See documentation below.
- Add a game store. I'll add some documentation below.
- ~ Implement Threads
  - To be honest, I think the deprecation of threads earlier caused a shift to a single-threaded scheme.
  - Could use threading for apps. Not sure how inputs would work.
- ~ Revamp Guest user!
  - ^ Make guest user more user-friendly. Remove "Games will say the path is invalid", make a workaround!
    - ^ Add guest folder, and ask user if they want to save data to a new user
  - ^ Add guest user at startup.
  - Allow guest user ALL THE TIME. Users should be able to select the guest user during Switch.
    - But make it like an Easter egg. Don't show it, but users CAN type guest if they want.
    - Same functionality as a guest. Make sure you can save during shutdown, create folders, etc.
- Fix recovery and streamline process.
  - Things like security, intentional corruption, the general process
  - Avoid hard resets AT ALL COSTS. We are not Apple.

# TODO - POCS4.0 after gamma01:
- In case I forget, mid-method saved_state is possible by saving each user input to a list, saved with each application.
  When the saved_state object is restored, the list will be checked. If there are items, they will be iterated and typed
  with pynput.keyboard.Controller().type() so that each input() can be filled with the respective inputs from the user
  and the state can be restored.

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
- X Each game will be iterated through and the individual user progress will be written to the database.
  - X Each game will now have game files, so no more saving through shutdown.
- Each game will also be completely internalized. Every parameter given to __init__ and boot are literals, no objects.
- X This is going to be really hard.
- ACTUALLY, Since every game is isolated and doesn't require anything, doing this is much easier.

## Registry Editor:
- Module, Class, and App to change global system/app settings.
- This combined with the game store with a fool-proof iteration protocol that will allow users to create their own apps, add to the registry, and use those registry entries!
- In the registry class, there will be a method to modify the registry.
  - Security risks will also be handled. Elevation will be considered and some kind of password will be required to make sure no one can make a game with registry-altering code.
- Before the module is created, I'll put it in Loading.

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