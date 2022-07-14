import os
from Applications import bagels
from System import Loading
from datetime import datetime as dt, timedelta as td
import calendar
import random

# TODO
# Add attributes for all possessions (if applicable).
# Add Rank.
# Add more events to the troop meeting and increase number shown to 4.
# Ask Appa and Amma for feedback!

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
possession_attributes = {"computer": "ScoutRPG.online_shopping = True",
                         "cell phone": "ScoutRPG.sleep_weight.extend([0] * 2 + [1] * 2) ; ScoutRPG.choices['self.phone()'] = 'phone'",
                         "digital watch": "ScoutRPG.sleep_weight.extend([0] * 6 + [1] * 7)",
                         "game console": "ScoutRPG.sleep_weight.extend([3] * 3 + [4] * 2) ; ScoutRPG.choices['self.console()'] = 'console'",
                         "camera": "ScoutRPG.sleep_weight.extend([4]) ; ScoutRPG.memories = True"}
department_costs = (17.5, 20.0, 15.0, 7.5, 50.0, 100.0,
                    500.0, 450.0, 15.0, 550.0, 200.0)
scout_store_list = ("pants", "shorts", "long-sleeve shirt", "short-sleeve shirt", "socks", "belt", "cap", "accessories",
                    "neckerchief", "slide", "handbook", "large tent", "sleeping bag", "sleeping pad", "camping pack",
                    "hiking sticks", "day pack", "scout water bottle", "insect repellent", "sunscreen", "compass",
                    "first aid kit", "pillow", "mess kit", "drinking cup")
scout_store_costs = (60.0, 24.0, 38.0, 27.0, 15.0, 20.0, 25.0, 20.0,
                     24.0, 150.0, 62.5, 27.5, 50.0, 42.5, 35,
                     20.0, 7.5, 5.5, 12.5, 17.5, 10.0, 15.0,
                     5.0)
event_list = {"troop meeting": "self.troop_meeting()"}


# Abilities for non-specialized possessions.
# Computer: Allows for online shopping (0 travel time for all stores)
# Cell phone: -25% chance of being late and oversleeping, and an option for recreation.
# Digital Watch: -50% chance of being late and oversleeping.
# Game console: +25% chance of being late and oversleeping, and an option for recreation.
# Camera: +5% chance of being late and oversleeping. Memories saved in game files.
# Full uniform (Pants/Shorts, Shirt, Socks, belt, optional cap) + handbook REQUIRED for troop meetings. If not present, player will be scolded. FUTURE: Will decrease reputation.

# Deprecated.
# days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Statistics:
    def __init__(self, stats=None):
        self.health = self.hunger = self.thirst = self.money = self.reputation = -1
        if stats:
            try:
                self.health = float(stats[0])
                self.hunger = float(stats[1])
                self.thirst = float(stats[2])
                self.money = float(stats[3])
                self.reputation = int(stats[4])
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
        try:
            exec([possession_attributes[i] for i in department_list if i == name][0])
        except KeyError:
            pass

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
    version = 'alpha1.4'
    sleep_weight = [0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4]
    choices = {'self.eat()': "eat", 'self.drink()': "drink", 'self.sleep()': "sleep", 'self.heal()': "heal",
               'self.house_chores()': "chores", 'self.travel()': "travel", 'self.agenda()': "agenda"}
    memories = False
    online_shopping = False

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
                # Deprecated.
                # self.stats = None
                # self.food = []
                # self.drinks = []
                # self.locations = []
                # self.possessions = []
                # stats will look something like "100.0\t50.0\t50.0\t0.0"
                self.stats = Statistics(stats.split('\t')) if stats else Statistics()
                # Food data looks like peanuts,5,5,5\tpancake10,10,15
                self.food = [Food(i.split(',')[0], i.split(',')[1]) for i in food.split('\t')] if food else []
                self.drinks = [Drink(i.split(',')[0], i.split(',')[1]) for i in drinks.split('\t')] if drinks else []
                self.locations = [Location(i.split(',')[0], i.split(',')[1]) for i in locations.split('\t')] if locations else []
                self.time = dt.strptime(time, "%m%d%Y%H%M") if time else None
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
        time = self.time.strftime("%m%d%Y%H%M")
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
        previous_time = self.time
        # Check if we're modifying time or updating it.
        if element and value:
            # Make sure the passed element is ok.
            if element in ("day", "hour", "minute"):
                self.time += td(days=value if element == "day" else 0,
                                hours=value if element == "hour" else 0,
                                minutes=value if element == "minute" else 0)
            # Math to calculate total time.
            self.difference[0] += abs(self.time - previous_time).total_seconds()
            self.difference[1] += abs(self.time - previous_time).total_seconds()
            if self.difference[0] >= 3600:
                self.stats.hunger -= 5 * (self.difference[0] / 3600)
                self.difference[0] = 0
            if self.difference[1] >= 1800:
                self.stats.thirst -= 5 * (self.difference[1] / 1800)
                self.difference[1] = 0
            if self.stats.hunger <= 0:
                self.difference[2] += (3600 * (abs(self.stats.hunger) / 600))
            if self.stats.thirst <= 0:
                self.difference[3] += (1800 * (abs(self.stats.thirst) / 300))
            if self.stats.hunger <= 0 and self.difference[2] >= 600:
                self.stats.health -= 1 * (self.difference[2] / 600)
                self.difference[2] = 0
            if self.stats.thirst <= 0 and self.difference[3] >= 300:
                self.stats.health -= 1 * (self.difference[3] / 300)
                self.difference[3] = 0
        else:
            # Capping each stat to 0 or 100.
            for i in self.stats.__iter__():
                if i != "money":
                    self.stats.__setattr__(i, 0.0) if self.stats.__getattribute__(i) < 0.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, 100.0) if self.stats.__getattribute__(i) > 100.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, self.stats.__getattribute__(i).__round__(1))
            # 1 Hour reminder for events!
            for i in self.events:
                if 0 > (self.time - i.date).total_seconds() > -3600:
                    Loading.returning("Less than one hour until {}!".format(i.name), 3)
                if (self.time - i.date).total_seconds() == 0:
                    try:
                        exec(event_list[i.name.lower()])
                    except KeyError:
                        pass
            else:
                # Adding the weekly troop meeting.
                if self.time.weekday() == 0 and sum([i.name == "Troop Meeting" for i in self.events]) < 0:
                    troop_meeting = Event("Troop Meeting", self.time.month + str(int(self.time.day) + 1) + self.time.year + '1900', 3)
                    self.events.append(troop_meeting)
                    Loading.returning("EVENT: Troop Meeting on {} at {}. Importance: {}".format(troop_meeting.str_date(), troop_meeting.str_time(), troop_meeting.importance), 3)
        # Daily stuff
        if self.time.day > previous_time.day:
            for i in self.chores:
                i.__setattr__('cooldown', False)
            self.stats.money += 25
            Loading.returning("ALLOWANCE: $25.00 has been added to your wallet.", 2)
        if self.stats.health <= 0.0:
            if self.defeat() == 1:
                self.setup()
            else:
                return 1

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
            version = 'alpha1.2'
            (stats, food, drinks, time, locations, chores, possessions) = datapack[1:]
            time = time.split(',')
            time = [list(calendar.day_name)[dt.strptime('{} {} {}'.format(time[0], time[1], time[2]), '%m %d %Y').weekday()]] + time
            time = ','.join(time)
            datapack = [version, stats, food, drinks, time, locations, chores, possessions, '']
        if version == 'alpha1.2':
            version = 'alpha1.3'
            (stats, food, drinks, time, locations, chores, possessions, events) = datapack[1:]
            time = time.split(',')
            time = time[1] + time[2] + time[3] + time[4] + time[5]
            new_possessions = []
            if possessions:
                possessions = possessions.split('\t')
                for i in range(len(possessions)):
                    if possessions[i] not in ("reusable plastic box", "reusable liquid flask", "kitchen cabinets", "refrigerator"):
                        new_possessions.append(possessions[i])
            new_possessions = '\t'.join(new_possessions)
            datapack = [version, stats, food, drinks, time, locations, chores, new_possessions, events]
        if version == 'alpha1.3':
            version = ScoutRPG.version
            (stats, food, drinks, time, locations, chores, possessions, events) = datapack[1:]
            stats += '\t0'
            datapack = [version, stats, food, drinks, time, locations, chores, possessions, events]
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
            print(self.time.strftime("\nDate: %A, %m/%d/%Y\nTime: %H:%M"))
            print('\n'.join(i + (": $" if i == "Money" else ": ") + str(self.stats.__getattribute__(i.lower())) for i in stats_list))
            action = input('What would you like to do? Type "help" for help').lower()
            if action == "help":
                input('Here is a list of common actions:\n1. Eat\n2. Drink\n3. Sleep\n4. Heal\n5. Chores\n6. Travel\n7. Agenda\n'
                      'You can type "exit" to exit')
            # Deprecated.
            # choices = {self.eat: "eat", self.drink: "drink", self.sleep: "sleep", self.heal: "heal",
            #            self.house_chores: "chores", self.travel: "travel", self.agenda: "agenda"}
            if action in ('quit', 'exit', 'leave', 'save'):
                self.quit()
                return
            for i in ScoutRPG.choices:
                if action == ScoutRPG.choices[i]:
                    print()
                    exec(i)
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
        self.time = dt.strptime("0301" + str(dt.today().year) + "0800", "%m%d%Y%H%M")
        # [list(calendar.day_name)[dt.strptime('03 01 {}'.format(dt.today().year), '%m %d %Y').weekday()], "3", "1", dt.today().year, "08", "00"]
        self.difference = [0, 0, 0, 0]
        self.locations = [Location(i, 10 * (self.locations.index(i) + 1)) for i in self.locations]
        self.chores = [Chore(i) for i in chore_list]
        self.possessions = []
        self.events = []

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
                self.refresh("minute", action.duration)
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
                self.refresh("minute", action.duration)
                Loading.returning("You drink a bottle of {}, and it was {}".format(action.name.title(), ["quenching", "tasty", "refreshing"][random.randint(0, 2)]), 2)
                if action.count <= 0:
                    self.drinks.pop(self.drinks.index(action))
                break
            except (IndexError, ValueError):
                Loading.returning("You do not have any bottles of {}!".format(action), 2)
        pass

    def sleep(self):
        if int(self.time.hour) >= 21 or int(self.time.hour) < 8:
            self.refresh("day", 1)
            self.time = self.time.replace(hour=8, minute=00)
            self.stats.hunger = 25 if self.stats.hunger > 25 else self.stats.hunger
            self.stats.thirst = 25 if self.stats.thirst > 25 else self.stats.thirst
            print("SLEEP: Until 8:00")
            Loading.returning("It's getting late, so you turn in for the day.", 3)
            Loading.returning("Zzzzzzz...", 3)
        else:
            sleep_time = ScoutRPG.sleep_weight[random.randint(0, len(ScoutRPG.sleep_weight) - 1)]
            if self.stats.hunger <= 0 or self.stats.thirst <= 0:
                Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you sleep.", 3)
            match sleep_time:
                case 0:
                    self.refresh("minute", 30)
                    print("SLEEP: 30 Minutes")
                    Loading.returning("You take a small nap and feel more energized.", 3)
                case 1:
                    self.refresh("hour", 1)
                    print("SLEEP: 1 Hour")
                    Loading.returning("You take a good nap and are ready to progress.", 3)
                case 2:
                    self.refresh("hour", 2)
                    print("SLEEP: 2 Hours")
                    Loading.returning("You sleep for a while after your alarm, but you still have time in the day.", 3)
                case 3:
                    self.refresh("hour", 3)
                    print("SLEEP: 3 Hours")
                    Loading.returning("You oversleep a little bit, but it's nothing special.", 3)
                case 4:
                    self.refresh("hour", 4)
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
                    self.refresh("minute", action.duration)
                    Loading.returning("Chore complete! ${}0 has been added to your wallet. You may not do this chore again today.".format(action.earnings), 3)
                    return
                else:
                    Loading.returning("You have already done that chore today!", 2)
            else:
                Loading.returning("Please enter a valid chore or press ENTER to return.", 2)

    def travel(self):
        if ScoutRPG.online_shopping:
            print("You have a computer! Welcome to Online Shopping.\nType the store you want to buy from.")
            print('\n'.join(str(i.name.title()) + ' --> 0 minutes' for i in self.locations))
            destination = input("Where would you like to go?").lower()
            destination = destination + " store" if "store" not in destination else destination
            for i in locations_list:
                if destination == i:
                    stores = (self.groceries, self.department, self.scout_store)
                    print("ONLINE: " + i.name.title())
                    stores[locations_list.index(i.name)]()
        else:
            print('\n'.join(str(i.name.title()) + ' --> ' + str(i.duration) + ' minutes' for i in self.locations))
            destination = input("Where would you like to go?").lower()
            destination = destination + " store" if "store" not in destination else destination
            for i in self.locations:
                if destination == i.name:
                    stores = (self.groceries, self.department, self.scout_store)
                    self.refresh("minute", i.duration)
                    Loading.progress_bar("Traveling to the {}".format(destination), i.duration / 4)
                    stores[locations_list.index(i.name)]()
                    self.refresh("minute", i.duration)
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
        print('\n'.join([i.name + " on " + i.date.strftime("%m/%d/%Y at %H:%M") + ". Importance: " + str(i.importance) for i in self.events]) if self.events else "No events.")
        print('\n' + calendar.TextCalendar(6).formatmonth(int(self.time.year), int(self.time.month)))
        if input('Type "add event" to add a custom event or Press ENTER to continue.') == 'add event':
            self.events.append(Event(input("What is the event name?"), input("Date and time of the event? E.g. 030120221900"), int(input("Importance of the event?"))))

    def troop_meeting(self):
        class MeetingEvent:
            def __init__(self, event, yes_msg, no_msg, reputation):
                self.event = event
                self.yes_msg = yes_msg
                self.no_msg = no_msg
                self.reputation = reputation
                self.answer = None

        Loading.returning("Welcome to the troop meeting.", 2)
        required_uniform = ["Shirt", "Pant", "Socks", "Belt", "Neckerchief", "Slide", "Shoes"]
        for i in self.possessions:
            for j in required_uniform:
                if i.name == j:
                    required_uniform.pop(j)
                    break
        if required_uniform:
            Loading.returning(["Your Scoutmaster was outside the door ", "An adult leader saw you walk in ", "Your friend was at your table "][random.randint(0, 2)] +
                              ["and noticed you didn't have your ", "and commented on your lack of ", "and scolded you for not having your "][random.randint(0, 2)] +
                              ', '.join(required_uniform) + '. Make sure you have it next meeting!', 5)
        Loading.returning("The flag ceremony has begun.", 2)
        for i in ('"Color Guard, Attention!"', '"Troop, Attention!"', '"Color Guard, forward march!"', '"Color Guard, halt!"',
                  '"Color Guard, prepare to post the colors!"', '"Scout hand salute!"', '"Please join me in the pledge of allegiance."',
                  '"I pledge allegiance to the flag of the United States of America. And to the Republic, for which it stands, '
                  'one nation, under God, indivisible, with Liberty and Justice for all."', '"Color Guard, Post the colors!"', '"Two!"    ',
                  '"Color Guard, about... face!"', '"Color Guard, reform!"', '"Color Guard, forward march!"', '"Color Guard, dismissed! Troop, at ease."'):
            Loading.returning(i, int(len(i) / 10))
        Loading.returning("The flag ceremony has ended.", 2)
        Loading.returning("You head to your table and sit down.", 2)
        # Deprecated.
        # for i in [("A friend approaches you and asks for your help. Yes or no?", "Your friend appreciates the help. He may ask you later.", "Your friend woefully walks away. He may ask you later.", 5),
        #           ("A surprise uniform inspection has occurred!", "", "", 0),
        #           ("Your patrol wants to organize an outing. Yes or no?", "Your patrol is grateful for your support.", "Your patrol scoffs at your laziness and continues their planning", 15),
        #           ("The scoutmaster is asking you if the meeting is going well. Yes or no?", "The scoutmaster is glad you enjoy the meeting.", "The scoutmaster is sorry you aren't having fun.", 10),
        #           ("You see your friend playing on his phone and think about telling him to stop. Yes or no?", "Your friend scoffs at you and puts it away. An adult leader comes by later, and your friend thanks you for the advice.",
        #            "Your friend continues to play and an adult leader comes by. They scold your friend and take away his phone.", 5),
        #           ("The weekly meeting game has begun. Are you going to participate? Yes or no?", "The game goes well. Your team wins and you are glad you participated.", "The game goes well, and everyone has fun. Everyone except you.", 20),
        #           ("You had a long day today and you are just about to fall asleep. Slap yourself awake? Yes or no?", "You slap yourself and your patrol looks at you. You explain it and they understand.",
        #            "You fall asleep and have a good dream. Thankfully, your patrol notices and wake you up before a leader comes by.", 10),
        #           ("You're getting bored and want to head to another table to socialize. Yes or no?", "You head to another table and start socializing. It goes well until a leader comes by and sends you back.",
        #            "You stay at your table and socialize with your own patrol.", -15),
        #           ("Your friend is going for a scoutmaster conference and asks for good luck. Yes or no?", "He thanks you for your wishes and heads off, feeling confident.", "Your friend walks away annoyed at you.", 5)]:
        #     events.append(MeetingEvent(i[0], i[1], i[2], i[3]))
        # yes = ["Your friend appreciates the help. He may ask you later.", None, "Your patrol is grateful for your support.",
        #        "The scoutmaster is glad you enjoy the meeting.", "Your friend scoffs at you and puts it away. An adult leader comes by later, and your friend thanks you for the advice.",
        #        "The game goes well. Your team wins and you are glad you participated.", "You slap yourself and your patrol looks at you. You explain it and they understand.",
        #        "You head to another table and start socializing. It goes well until a leader comes by and sends you back.", "He thanks you for your wishes and heads off, feeling confident."]
        # no = ["Your friend woefully walks away. He may ask you later.", None, "Your patrol scoffs at your laziness and continues their planning",
        #       "The scoutmaster is sorry you aren't having fun.", "Your friend continues to play and an adult leader comes by. They scold your friend and take away his phone.",
        #       "The game goes well, and everyone has fun. Everyone except you.", "You fall asleep and have a good dream. Thankfully, your patrol notices and wake you up before a leader comes by.",
        #       "You stay at your table and socialize with your own patrol.", "Your friend walks away annoyed at you."]
        for i in random.sample(
                [MeetingEvent(i[0], i[1], i[2], i[3]) for i in [("A friend approaches you and asks for your help. Yes or no?", "Your friend appreciates the help. He may ask you later.", "Your friend woefully walks away. He may ask you later.", 5),
                                                                ("A surprise uniform inspection has occurred!", "", "", 0),
                                                                ("Your patrol wants to organize an outing. Yes or no?", "Your patrol is grateful for your support.", "Your patrol scoffs at your laziness and continues their planning", 15),
                                                                ("The scoutmaster is asking you if the meeting is going well. Yes or no?", "The scoutmaster is glad you enjoy the meeting.", "The scoutmaster is sorry you aren't having fun.", 10),
                                                                ("You see your friend playing on his phone and think about telling him to stop. Yes or no?",
                                                                 "Your friend scoffs at you and puts it away. An adult leader comes by later, and your friend thanks you for the advice.",
                                                                 "Your friend continues to play and an adult leader comes by. They scold your friend and take away his phone.", 5),
                                                                ("The weekly meeting game has begun. Are you going to participate? Yes or no?", "The game goes well. Your team wins and you are glad you participated.",
                                                                 "The game goes well, and everyone has fun. Everyone except you.", 20),
                                                                ("You had a long day today and you are just about to fall asleep. Slap yourself awake? Yes or no?", "You slap yourself and your patrol looks at you. You explain it and they understand.",
                                                                 "You fall asleep and have a good dream. Thankfully, your patrol notices and wake you up before a leader comes by.", 10),
                                                                ("You're getting bored and want to head to another table to socialize. Yes or no?", "You head to another table and start socializing. It goes well until a leader comes by and sends you back.",
                                                                 "You stay at your table and socialize with your own patrol.", -15),
                                                                ("Your friend is going for a scoutmaster conference and asks for good luck. Yes or no?", "He thanks you for your wishes and heads off, feeling confident.",
                                                                 "Your friend walks away annoyed at you.", 5)]], 4):
            if "Yes or no" in i.event:
                print(i.event)
                if input().lower() == "yes":
                    exec("Loading.returning(i.yes_msg, 3) ; Loading.returning('+{} Reputation.'.format(i.reputation), 2) ; self.stats.reputation += i.reputation")
                else:
                    exec("Loading.returning(i.no_msg, 3) ; Loading.returning('-{} Reputation.'.format(i.reputation), 2) ; self.stats.reputation -= i.reputation")
            else:
                Loading.returning(i.event, 3)
        input("The troop meeting has ended." + (" Don't forget to purchase the remaining uniform articles!" if required_uniform else "") + " Press ENTER to head back home.")
        self.events.pop(self.events.index([i for i in self.events if i.name == 'Troop Meeting'][0]))
        self.time = self.time.replace(hour=20, minute=00)
        self.stats.hunger = 40 if self.stats.hunger > 40 else self.stats.hunger
        self.stats.thirst = 40 if self.stats.thirst > 40 else self.stats.thirst

    def phone(self):
        phone_time = (random.randint(0, 3) + 1) * 15
        if self.stats.hunger <= 0 or self.stats.thirst <= 0:
            Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you use the phone.", 3)
        self.refresh("minute", phone_time)
        print("PHONE: {} Minutes".format(phone_time))
        Loading.returning(["You play on your phone for a bit.", "You have a nice phone session looking at memes.",
                           "You spend 45 whole minutes scrolling on social media.",
                           "Oops! You overspend your phone time and use up an hour."][int(phone_time / 15) - 1], 3)

    def console(self):
        console_time = (random.randint(0, 3) + 1) * 20
        if self.stats.hunger <= 0 or self.stats.thirst <= 0:
            Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you play games.", 3)
        self.refresh("minute", console_time)
        print("GAME CONSOLE: {} Minutes".format(console_time))
        Loading.returning(["You take a quick break and play some games.", "You play for quite a bit and have some good fun.",
                           "You spend an hour playing with friends and having a great time.",
                           "Oops! You lose track of time and play for a while. It was still fun"
                           "."][int(console_time / 20) - 1], 3)

    def defeat(self):
        Loading.returning("Oh no!", 2)
        Loading.returning("Your health is very low.", 2)
        if self.stats.hunger == 0.0:
            Loading.returning("You are extremely hungry.", 2)
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
