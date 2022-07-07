import os
from Applications import bagels
from System import Loading
from datetime import datetime as dt
import calendar
import random

stats_list = ("Health", "Hunger", "Thirst", "Money")
food_list = {"peanuts", "breakfast burrito", "pancake", "mac and cheese", "tofu teriyaki"}
food_costs = (0.5, 3.5, 2.5, 9.5, 15.0)
drinks_list = ("water", "soda")
drinks_cost = (0.25, 1.5)
locations_list = ("grocery store", "department store", "scout store")
chore_list = {"unload dishwasher": (5.0, 15), "load dishwasher": (10.0, 30), "clean up bedroom": (7.5, 25),
              "clean up kitchen": (15.0, 40), "clean up dining room": (8.5, 30), "clean up living room": (7.5, 20),
              "collect the trash": (10.0, 10)}
department_list = ("rugged pants", "rugged jacket", "full body thermals", "hiking socks", "desk", "tent",
                   "computer", "cell phone", "digital watch", "game console", "camera")
department_costs = (17.5, 20.0, 15.0, 7.5, 50.0, 100.0,
                    500.0, 450.0, 15.0, 550.0, 200.0)
scout_store_list = ("pants", "shorts", "long-sleeve shirt", "short-sleeve shirt", "socks", "belt", "cap", "accessories",
                    "handbook", "large tent", "sleeping bag", "sleeping pad", "camping pack", "hiking sticks", "day pack",
                    "scout water bottle", "insect repellent", "sunscreen", "compass", "first aid kit", "pillow", "mess kit",
                    "drinking cup")
scout_store_costs = (60.0, 24.0, 38.0, 27.0, 15.0, 20.0, 25.0, 20.0,
                     24.0, 150.0, 62.5, 27.5, 50.0, 42.5, 35,
                     20.0, 7.5, 5.5, 12.5, 17.5, 10.0, 15.0,
                     5.0)
# Abilities for non-specialized possessions.
# Computer: Allows for online shopping (0 travel time for all stores)
# Cell phone: -25% chance of being late and oversleeping, and an option for recreation.
# Digital Watch: -50% chance of being late and oversleeping.
# Game console: +25% chance of being late and oversleeping, and an option for recreation.
# Camera: +5% chance of being late and oversleeping. Memories saved in game files.
# Full uniform (Pants/Shorts, Shirt, Socks, belt, optional cap) + handbook REQUIRED for troop meetings. If not present, player will be scolded. FUTURE: Will decrease reputation.
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Statistics:
    def __init__(self, stats=None):
        self.health = self.hunger = self.thirst = self.money = -1
        if stats:
            try:
                self.health = float(stats[0])
                self.hunger = float(stats[1])
                self.thirst = float(stats[2])
                self.money = float(stats[3])
            except IndexError:
                pass
        else:
            self.health = 100.0
            self.hunger = 50.0
            self.thirst = 50.0
            self.money = 0.0

    @staticmethod
    def __iter__():
        return ['health', 'hunger', 'thirst', 'money']


class Food:
    def __init__(self, name=None, count=None):
        self.name = name if name else None
        match self.name:
            case 'peanuts':
                (self.count, self.fuel, self.duration) = (5, 5, 5)
            case 'breakfast burrito':
                (self.count, self.fuel, self.duration) = (0, 10, 10)
            case 'pancake':
                (self.count, self.fuel, self.duration) = (10, 10, 15)
            case 'mac and cheese':
                (self.count, self.fuel, self.duration) = (0, 20, 30)
            case 'tofu teriyaki':
                (self.count, self.fuel, self.duration) = (0, 30, 35)
            case _:
                (self.count, self.fuel, self.duration) = (100, 100, 100)
        self.count = int(count) if count else self.count

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))

    def __iter__(self):
        return [self.name, self.count, self.fuel, self.duration]


class Drink:
    def __init__(self, name=None, count=None):
        self.name = name if name else None
        match self.name:
            case 'water':
                (self.count, self.fuel, self.duration) = (24, 20, 5)
            case 'soda':
                (self.count, self.fuel, self.duration) = (0, 100, 10)
            case _:
                (self.count, self.fuel, self.duration) = (0, 0, 0)
        self.count = int(count) if count else self.count

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))

    def __iter__(self):
        return [self.name, self.count, self.fuel, self.duration]


class Location:
    def __init__(self, name=None, duration=None):
        self.name = name
        self.duration = int(duration)

    def __repr__(self):
        return self.name + ',' + str(self.duration)


class Chore:
    def __init__(self, name=None, cooldown=False):
        self.name = name
        match self.name:
            case 'unload dishwasher':
                (self.earnings, self.duration) = (5.0, 15)
            case 'load dishwasher':
                (self.earnings, self.duration) = (10.0, 30)
            case 'clean up bedroom':
                (self.earnings, self.duration) = (7.5, 25)
            case 'clean up kitchen':
                (self.earnings, self.duration) = (15, 40)
            case 'clean up dining room':
                (self.earnings, self.duration) = (8.5, 30)
            case 'clean up living room':
                (self.earnings, self.duration) = (7.5, 20)
            case 'collect the trash':
                (self.earnings, self.duration) = (10.0, 10)
        self.cooldown = cooldown == "True"

    def __repr__(self):
        return self.name + ',' + str(self.cooldown)


class Possession:
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name


class Event:
    def __init__(self, name=None, date=None, importance=None):
        self.name = name
        self.date = dt.strptime(date, '%m%d%Y%H%M')
        self.importance = importance

    def __repr__(self):
        return self.name + ',' + self.date.strftime('%m%d%Y%H%M') + ',' + str(self.importance)

    def str_date(self):
        return self.date.strftime("%m-%d-%Y")

    def str_time(self):
        return self.date.strftime("%H:%M")


class ScoutRPG:
    category = "games"
    version = 'alpha1.2'

    @staticmethod
    def boot(path='\\'):
        scout_rpg = ScoutRPG(path)
        if not scout_rpg.filename == "exit":
            scout_rpg.main()

    def __init__(self, path):
        # Default game setup code, pulled from sonar.py.
        self.new_file = False
        self.filename = ""
        self.path = path
        game_info = bagels.init_game(self, path, 'sct')
        # Default stats for the time being. Health, Hunger, Thirst, and time (date, hour, minute).
        if game_info:
            # Decrypting everything and cutting off the new line at the end!
            try:
                version = Loading.caesar_decrypt(game_info[0]).split('\n')[0]
            except IndexError:
                input("There is no version in the selected game file. Press ENTER to delete it, or stop the program now "
                      "to attempt to recover progress by yourself.")
                os.remove(self.path + '\\' + self.filename)
                return
            try:
                # Checking for update and unpacking...
                (version, stats, food, drinks, time, locations, chores, possessions, events) = self.update_check(version, [Loading.caesar_decrypt(i).split('\n')[0] for i in game_info])
                self.stats = None
                self.food = []
                self.drinks = []
                self.locations = []
                self.possessions = []
                # stats will look something like "100.0\t50.0\t50.0\t0.0"
                self.stats = Statistics(stats.split('\t')) if stats else Statistics()
                # Food data looks like peanuts,5,5,5\tpancake10,10,15
                self.food = [Food(i.split(',')[0], i.split(',')[1]) for i in food.split('\t')] if food else []
                self.drinks = [Drink(i.split(',')[0], i.split(',')[1]) for i in drinks.split('\t')] if drinks else []
                self.locations = [Location(i.split(',')[0], i.split(',')[1]) for i in locations.split('\t')] if locations else []
                self.time = time.split('\n')[0].split(',') if time else None
                self.previous_time = self.time.copy()
                self.difference = [0, 0, 0, 0]
                self.chores = [Chore(i.split(',')[0], i.split(',')[1]) for i in chores.split('\t')] if chores else []
                self.possessions = [Possession(i) for i in possessions.split('\t')] if possessions else []
                self.events = [Event(i.split(',')[0], i.split(',')[1], i.split(',')[2]) for i in events.split('\t')] if events else []
            except (KeyError, IndexError, ValueError):
                # If the element doesn't exist.
                input("This game save is corrupted! Nooooo...\nPress ENTER to delete it, or stop the program now "
                      "to attempt to recover progress by yourself.")
                os.remove(self.path + '\\' + self.filename)
                return

    def quit(self):
        if self.new_file:
            self.filename = input("File name?\n") + '.sct'
        stats = '\t'.join(str(self.stats.__getattribute__(i)) for i in self.stats.__iter__())
        food = '\t'.join(i.__repr__() for i in self.food)
        drinks = '\t'.join(i.__repr__() for i in self.drinks)
        time = ','.join(self.time)
        locations = '\t'.join(i.__repr__() for i in self.locations)
        chores = '\t'.join(i.__repr__() for i in self.chores)
        possessions = '\t'.join(i.__repr__() for i in self.possessions)
        events = '\t'.join(i.__repr__() for i in self.events)
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            for i in (ScoutRPG.version, stats, food, drinks, time, locations, chores, possessions, events):
                game.write(Loading.caesar_encrypt(i) + '\n')
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
        return

    def refresh(self, element=None, value=None):
        for i in range(1, len(self.time)):
            self.time[i] = int(self.time[i])
        self.previous_time = self.time.copy()
        # Check if we're modifying time or updating it.
        if element and value:
            # Make sure the passed element is ok.
            if 1 <= element <= 5:
                self.time[element] += value
            # Math to calculate total time.
            self.difference[0] += abs(((60 * self.time[4]) + self.time[5]) - ((60 * self.previous_time[4]) + self.previous_time[5]))
            self.difference[1] += abs(((60 * self.time[4]) + self.time[5]) - ((60 * self.previous_time[4]) + self.previous_time[5]))
            if self.difference[0] >= 60:
                self.stats.hunger -= 5 * (self.difference[0] / 60)
                self.difference[0] = 0
            if self.difference[1] >= 30:
                self.stats.thirst -= 5 * (self.difference[1] / 30)
                self.difference[1] = 0
            if self.stats.hunger <= 0:
                self.difference[2] += (60 * (abs(self.stats.hunger) / 5))
            if self.stats.thirst <= 0:
                self.difference[3] += (30 * (abs(self.stats.thirst) / 5))
            if self.stats.hunger <= 0 and self.difference[2] >= 10:
                self.stats.health -= 1 * (self.difference[2] / 10)
                self.difference[2] = 0
            if self.stats.thirst <= 0 and self.difference[3] >= 5:
                self.stats.health -= 1 * (self.difference[3] / 5)
                self.difference[3] = 0
        else:
            # Update the time.
            # Hour rollover
            if self.time[5] >= 60:
                self.time[5] -= 60
                self.time[4] += 1
            # Day Rollover
            if self.time[4] >= 24:
                self.time[4] -= 24
                self.time[2] += 1
            # Month rollover
            if self.time[2] >= days[self.time[1] - 1]:
                self.time[2] -= days[self.time[1] - 1]
                self.time[1] += 1
            # Year rollover
            if self.time[1] >= 12:
                self.time[1] -= 12
                self.time[3] += 1
            # Updating stats
            for i in self.stats.__iter__():
                if i != "money":
                    self.stats.__setattr__(i, 0.0) if self.stats.__getattribute__(i) < 0.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, 100.0) if self.stats.__getattribute__(i) > 100.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, self.stats.__getattribute__(i).__round__(1))
        # Daily stuff
        if self.time[2] > self.previous_time[2]:
            for i in self.chores:
                i.__setattr__('cooldown', False)
            self.stats.money += 25
            Loading.returning("ALLOWANCE: $25.00 has been added to your wallet.", 2)
        if self.stats.health <= 0.0:
            if self.defeat() == 1:
                self.setup()
            else:
                return 1
        for i in range(1, len(self.time)):
            if self.time[i] < 10:
                self.time[i] = "0" + str(int(self.time[i]))
            else:
                self.time[i] = str(int(self.time[i]))
        self.time[0] = list(calendar.day_name)[dt.strptime('{} {} {}'.format(self.time[1], self.time[2], self.time[3]), '%m %d %Y').weekday()]
        for i in self.events:
            if i.name == "Troop Meeting":
                break
        else:
            if self.time[0] == "Sunday":
                troop_meeting = Event("Troop Meeting", self.time[1] + str(int(self.time[2]) + 1) + self.time[3] + '1900', 3)
                self.events.append(troop_meeting)
                Loading.returning("EVENT: Troop Meeting on {} at {}. Importance: {}".format(troop_meeting.str_date(), troop_meeting.str_time(), troop_meeting.importance), 3)
        self.previous_time = self.time.copy()

    def update_check(self, version, datapack):
        # "Recursive" method to upgrade game files saved in previous versions.
        if version == 'prealpha':
            version = 'alpha1.0'
            (stats, food, drinks, time) = datapack[1:]
            stats = '\t'.join(stats.split(',')) + '\t0.0'
            food = food.split('\t')
            for i in range(len(food)):
                match food[i].split(',')[2]:
                    case '5':
                        food[i] = 'peanuts,' + food[i]
                    case '10':
                        food[i] = 'breakfast burrito,' + food[i]
                    case '15':
                        food[i] = 'pancake,' + food[i]
                    case '30':
                        food[i] = 'mac and cheese,' + food[i]
                    case '35':
                        food[i] = 'tofu teriyaki,' + food[i]
            food = '\t'.join(food)
            drinks = drinks.split('\t')
            for i in range(len(drinks)):
                match drinks[i].split(',')[2]:
                    case '5':
                        drinks[i] = 'water,' + drinks[i]
                    case '10':
                        drinks[i] = 'soda,' + drinks[i]
            drinks = '\t'.join(drinks)
            locations = 'grocery store,10\tdepartment store,20\tscout store,30'
            chores = '\t'.join(i + ',False' for i in chore_list)
            possessions = ''
            datapack = [version, stats, food, drinks, time, locations, chores, possessions]
        if version == 'alpha1.0':
            version = 'alpha1.1'
            (stats, food, drinks, time, locations, chores, possessions) = datapack[1:]
            if possessions:
                possessions = possessions.split('\t')
                for i in range(len(possessions)):
                    (name, quantity) = possessions[i].split(',')
                    possessions[i] = '\t'.join([name] * int(quantity))
                possessions = '\t'.join(possessions)
            datapack = [version, stats, food, drinks, time, locations, chores, possessions]
        if version == 'alpha1.1':
            version = ScoutRPG.version
            (stats, food, drinks, time, locations, chores, possessions) = datapack[1:]
            time = time.split(',')
            time = [list(calendar.day_name)[dt.strptime('{} {} {}'.format(time[0], time[1], time[2]), '%m %d %Y').weekday()]] + time
            time = ','.join(time)
            datapack = [version, stats, food, drinks, time, locations, chores, possessions, '']
            # Now to quit and rewrite the game files.
            # TODO THIS SHOULD BE MOVED TO THE BOTTOM OF THE UPGRADE TREE
            file = open(self.path + '\\' + self.filename, 'w')
            for i in datapack:
                file.write(Loading.caesar_encrypt(i) + '\n')
            file.close()
            Loading.returning("This game was saved in an older version of ScoutRPG. The save file will now be updated.", 3)
        return datapack

    def main(self):
        # Setup logic
        if self.new_file:
            self.setup()
        while True:
            if self.refresh() == 1:
                return
            # Status report. Date, time, all stats.
            print("\nDate: {}, {}/{}/{}\nTime: {}:{}.".format(self.time[0], self.time[1], self.time[2], self.time[3], self.time[4], self.time[5]))
            print('\n'.join(i + (": $" if i == "Money" else ": ") + str(self.stats.__getattribute__(i.lower())) for i in stats_list))
            action = input('What would you like to do? Type "help" for help').lower()
            if action == "help":
                input('Here is a list of common actions:\n1. Eat\n2. Drink\n3. Sleep\n4. Heal\n5. Chores\n6. Travel\n7. Agenda\n'
                      'You can type "exit" to exit')
            choices = {self.eat: "eat", self.drink: "drink", self.sleep: "sleep", self.heal: "heal",
                       self.house_chores: "chores", self.travel: "travel", self.agenda: "agenda"}
            if action in ('quit', 'exit', 'leave', 'save'):
                self.quit()
                return
            for i in choices:
                if action == choices[i]:
                    print()
                    i()
                    break

    def setup(self):
        if 'yes' in input("Would you like to view the premise?").lower():
            input("Welcome to Scouting!\nYou have embarked on a journey far beyond any other. Your physical and mental skills "
                  "will be tested. Your memory will be trained. Your survival instinct will be brought to life.\nPress ENTER "
                  "to continue.")
            input("\nYou are a boy scout, fresh out of cub scouts and ready to start your journey to Eagle. You need to show that you "
                  "are worthy of this rank by going to meetings, outings, camping trips, conferences, and service projects. These "
                  "are all events you can do to advance yourself.\nPress ENTER to continue.")
            input("\nYou have 6 main statistics: Health, Hunger, Thirst, Money, Agenda, and Rank.\nHEALTH is your body health. It can "
                  "be influenced by hunger, thirst, injuries, and first aid kits.\nHUNGER is how hungry you are. It can be influenced "
                  "by food.\nTHIRST is how thirsty you are. It can be influenced by beverages.\nMONEY is how much money you have. You "
                  "can do chores to get money, but you need money to buy things as well.\nAGENDA is your schedule for the day. It will "
                  "include events that you signed up for and should attend.\nRANK is your current Boy Scout Rank. The ranks are (in "
                  "order): Scout, Tenderfoot, Second Class, First Class, Star, Life, Eagle.\nPress ENTER to continue.")
            input("Your ultimate goal is to reach Eagle Scout and you have 7 years to do it. You are 11 years old, and you age out "
                  "at 18 years old. Good luck!")
        home = input("Would you like your home to be closer to the grocery store, department store, or scout store? "
                     "\nThe default is closer to the grocery store")
        if home in ("department", "department store"):
            self.locations = ("department store", "scout store", "grocery store")
        elif home in ("scout", "scout store"):
            self.locations = ("scout store", "grocery store", "department store")
        else:
            self.locations = ("grocery store", "department store", "scout store")
        self.stats = Statistics()
        self.food = [Food(i) for i in ("peanuts", "pancake")]
        self.drinks = [Drink("water")]
        self.time = [list(calendar.day_name)[dt.strptime('03 01 {}'.format(dt.today().year), '%m %d %Y').weekday()], "3", "1", dt.today().year, "08", "00"]
        self.previous_time = self.time.copy()
        self.difference = [0, 0, 0, 0]
        self.locations = [Location(i, 10 * (self.locations.index(i) + 1)) for i in self.locations]
        self.chores = [Chore(i) for i in chore_list]
        self.possessions = []

    def eat(self):
        print("Here's the food you have:")
        print('\n'.join("{} {} meals".format(str(int(i.count)).title(), i.name) for i in self.food if i.count > 0))
        while True:
            action = input("What would you like to eat?").lower()
            if not action:
                return
            try:
                action = [i for i in self.food if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                action.count -= 1
                self.stats.hunger += action.fuel
                self.refresh(5, action.duration)
                Loading.returning("You eat a {} meal, and it was {}".format(action.name.title(), ["tasty", "delicious", "scrumptious"][random.randint(0, 2)]), 2)
                if action.count <= 0:
                    self.food.pop(self.food.index(action))
                break
            except (IndexError, ValueError):
                Loading.returning("You don't have any {} meals!".format(action), 2)
        pass

    def drink(self):
        print("Here are the beverages you have:")
        print('\n'.join("{} bottles of {}".format(str(int(i.count)).title(), i.name) for i in self.drinks if i.count > 0))
        while True:
            action = input("What would you like to drink?").lower()
            if not action:
                return
            try:
                action = [i for i in self.drinks if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                action.count -= 1
                self.stats.thirst += action.fuel
                self.refresh(5, action.duration)
                Loading.returning("You drink a bottle of {}, and it was {}".format(action.name.title(), ["quenching", "tasty", "refreshing"][random.randint(0, 2)]), 2)
                if action.count <= 0:
                    self.drinks.pop(self.drinks.index(action))
                break
            except (IndexError, ValueError):
                Loading.returning("You do not have any bottles of {}!".format(action), 2)
        pass

    def sleep(self):
        if int(self.time[4]) >= 21 or int(self.time[4]) < 8:
            self.refresh(2, 1)
            self.time[4] = "08"
            self.time[5] = "00"
            self.stats.hunger = 25 if self.stats.hunger > 25 else self.stats.hunger
            self.stats.thirst = 25 if self.stats.thirst > 25 else self.stats.thirst
            print("SLEEP: Until 8:00")
            Loading.returning("It's getting late, so you turn in for the day.", 3)
            Loading.returning("Zzzzzzz...", 3)
        else:
            sleep_time = [random.randint(0, 10)]
            if self.stats.hunger <= 0 or self.stats.thirst <= 0:
                Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you sleep.", 3)
            match sleep_time:
                case 0, 1, 2:
                    self.refresh(5, 30)
                    print("SLEEP: 30 Minutes")
                    Loading.returning("You take a small nap and feel more energized.", 3)
                case 3, 4, 5, 6:
                    self.refresh(4, 1)
                    print("SLEEP: 1 Hour")
                    Loading.returning("You take a good nap and are ready to progress.", 3)
                case 7, 8:
                    self.refresh(4, 2)
                    print("SLEEP: 2 Hours")
                    Loading.returning("You oversleep a little bit, but it's nothing special.", 3)
                case 9:
                    self.refresh(4, 3)
                    print("SLEEP: 3 Hours")
                    Loading.returning("You sleep for a while after your alarm, but you still have time in the day.", 3)
                case 10:
                    self.refresh(4, 4)
                    print("SLEEP: 4 Hours")
                    Loading.returning("Oops! You oversleep a lot and are quite hungry.", 3)

    def heal(self):
        if self.stats.health < 100.0:
            self.stats.health = 100.0
            Loading.returning("You use a small first aid kit, food, and water to replenish yourself.", 3)
            Loading.returning("Make sure to eat and drink regularly!", 2)
        else:
            Loading.returning("You don't need to heal!", 2)

    def house_chores(self):
        print('\n'.join(str(i.name.title()) + " - +$" + str(i.earnings) + ' --> ' + str(i.duration) + ' minutes' + (", READY" if not i.cooldown else '') for i in self.chores))
        while True:
            action = input("Which chore do you want to do?")
            if not action:
                return
            elif action in chore_list:
                action = [i for i in self.chores if i.name == action][0]
                if not action.cooldown:
                    action.__setattr__('cooldown', True)
                    Loading.progress_bar(action.name.title().split(' ')[0] + 'ing ' + action.name.title().split(' ', 1)[1], action.duration / 4)
                    self.stats.money += action.earnings
                    self.refresh(5, action.duration)
                    Loading.returning("Chore complete! ${}0 has been added to your wallet. You may not do this chore again today.".format(action.earnings), 3)
                    return
                else:
                    Loading.returning("You have already done that chore today!", 2)
            else:
                Loading.returning("Please enter a valid chore or press ENTER to return.", 2)

    def travel(self):
        print('\n'.join(str(i.name.title()) + ' --> ' + str(i.duration) + ' minutes' for i in self.locations))
        destination = input("Where would you like to go?").lower()
        destination = destination + " store" if "store" not in destination else destination
        for i in locations_list:
            if destination == i:
                stores = (self.groceries, self.department, self.scout_store)
                self.refresh(5, [i.duration for i in self.locations if i.name == destination][0])
                Loading.progress_bar("Traveling to the {}".format(destination), [i.duration for i in self.locations if i.name == destination][0] / 4)
                stores[locations_list.index(i)]()
                self.refresh(5, [i.duration for i in self.locations if i.name == destination][0])
                break
        else:
            Loading.returning("Please pick a valid destination.", 2)

    def groceries(self):
        print("\n\nWelcome to the grocery store!")
        Loading.returning("Here you can buy food and drinks.", 2)
        print('\nFOOD')
        print('\n'.join(str(food_list.index(food_list[i]) + 1) + '. ' + food_list[i].title() + ' - $' + str(food_costs[i]) + '0' for i in range(len(food_list))))
        print('\nDRINKS')
        print('\n'.join(str(drinks_list.index(drinks_list[i]) + 1) + '. ' + drinks_list[i].title() + ' - $' + str(drinks_cost[i]) + '0' for i in range(len(drinks_list))))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "grocery store"][0] / 4)
                return
            elif buy in food_list:
                if self.buy(buy, self.food, food_list, food_costs, Food) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "grocery store"][0] / 4)
                    break
            elif buy in drinks_list:
                if self.buy(buy, self.drinks, drinks_list, drinks_cost, Drink) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "grocery store"][0] / 4)
                    break
            else:
                Loading.returning("Please type a valid food/drink.")

    def department(self):
        print("\n\nWelcome to the Department store!")
        Loading.returning("Here you can buy various utilities to add to your lifestyle.", 3)
        print("\nSTORAGE")
        print('\n'.join((str(department_list.index(i) + 1) + '. ' + i.title() + ': $' + str(department_costs[department_list.index(i)]) + '0') for i in department_list[0:3]))
        print("\nAPPLIANCES")
        print('\n'.join((str(department_list.index(i) - 2) + '. ' + i.title() + ': $' + str(department_costs[department_list.index(i)]) + '0') for i in department_list[3:]))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "department store"][0] / 4)
                return
            elif buy in department_list:
                if self.buy(buy, self.possessions, department_list, department_costs, Possession) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "department store"][0] / 4)
                    break
            else:
                Loading.returning("Please type a valid food/drink.")
        # Buy Utilities. Everything bought here is stored as objects in a list: self.possessions.
        # Desk: $50 - Reduces time needed to study for ranks.
        # Reusable Plastic Box: $25 - +5 food space.
        # Reusable Liquid Flask: $25 - +5 drinks space
        # Computer: $450 - Reduces time to study for ranks + Ability to purchase things online! - ONE TIME
        # Kitchen Cabinets: $350 - +20 Food space, +10 Drinks space - ONE TIME
        # Refrigerator: $550 - +15 drinks space, +10 food space - ONE TIME
        pass

    def scout_store(self):
        print('\nWelcome to the Scout Store!')
        Loading.returning("Here you can buy your various scouting equipment.", 2)
        print('\nSCOUT-BRANDED CLOTHING')
        print('\n'.join((str(scout_store_list.index(i) + 1) + '. ' + i.title() + ': $' + str(scout_store_costs[scout_store_list.index(i)]) + '0') for i in scout_store_list[0:7]))
        print('\nOUTDOORS')
        print('\n'.join((str(i - 7) + '. ' + scout_store_list[i].title() + ': $' + str(scout_store_costs[i]) + '0') for i in range(len(scout_store_list))[8:]))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "scout store"][0] / 4)
                return
            elif buy in scout_store_list:
                if self.buy(buy, self.possessions, scout_store_list, scout_store_costs, Possession) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "scout store"][0] / 4)
                    break
            else:
                Loading.returning("Please type a valid food/drink.")

    def buy(self, buy, stat, store_list, store_costs, item):
        while True:
            quantity = input('How many {} would you like? Type "exit" to exit.'.format(buy))
            if quantity == 'exit':
                return
            else:
                try:
                    quantity = int(quantity)
                except TypeError:
                    Loading.returning("Please type a number between 0 and 100.", 2)
                    continue
            if 0 <= quantity <= 100.0:
                if self.stats.money >= (quantity * store_costs[store_list.index(buy)]):
                    self.stats.money -= (quantity * store_costs[store_list.index(buy)])
                    try:
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count += quantity
                    except IndexError:
                        stat.append(item(buy))
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count = quantity
                    Loading.returning("Purchase successful. Your total was: ${}0".format(str(quantity * store_costs[store_list.index(buy)])), 2)
                    return
                else:
                    Loading.returning("You don't have enough money! ({})".format(self.stats.money), 2)
                    break
            else:
                Loading.returning("Please type a number between 0 and 100.", 2)

    def agenda(self):
        print('\n'.join([i.name + " on " + i.str_date() + " at " + i.str_time() + ". Importance: " + str(i.importance) for i in self.events]))
        print('\n' + calendar.TextCalendar(6).formatmonth(int(self.time[3]), int(self.time[1])))
        if input("Press ENTER to continue.") == 'debug':
            self.events.append(Event(input("What is the event name?"), input("Date and time of the event? E.g. 030120221900"), int(input("Importance of the event?"))))

    def defeat(self):
        Loading.returning("Oh no!", 2)
        if self.stats.hunger == 0.0:
            Loading.returning("You are extremely hungry.")
            if self.stats.thirst == 0.0:
                Loading.returning("You are also extremely dehydrated.", 2)
        elif self.stats.thirst == 0.0:
            Loading.returning("You are extremely dehydrated.", 2)
        Loading.returning("In order to remedy the problem, you are rushed to the emergency room.", 3)
        Loading.returning("Fortunately, they were successful.", 2)
        Loading.returning("However, your condition will never permit you to pursue Scouts ever again.", 3)
        Loading.returning("DEFEAT: Your scouting journey was ended prematurely and you will never reach your ultimate goal of the Eagle Rank.", 5)
        input("Press ENTER to delete your game file.")
        if not self.new_file:
            os.remove(self.path + '\\' + self.filename)
        if 'yes' in input("Would you like to try again?"):
            return 1
        else:
            Loading.returning_to_apps()
            return 0
