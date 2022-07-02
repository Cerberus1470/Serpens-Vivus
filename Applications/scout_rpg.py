import os
from Applications import bagels
from System import Loading
from datetime import datetime
import random

stats_list = ("Health", "Hunger", "Thirst", "Money")
food_list = ("peanuts", "breakfast burrito", "pancake", "mac and cheese", "tofu teriyaki")
food_costs = (2.5, 5.0, 3.5, 10.0, 20.0)
drinks_list = ("water", "soda")
drinks_cost = (1.0, 2.5)
locations_list = ("grocery store", "department store", "scout store")
chore_list = ("dish_unload", "dish_load", "clean_bed", "clean_kit", "clean_dine", "clean_live", "trash")
department_list = ("desk", "reusable plastic box", "reusable liquid flask", "computer", "kitchen cabinets", "refrigerator")
department_costs = (50.0, 25.0, 25.0, 450.0, 350.0, 550.0)
scout_store_list = ("pants", "shorts", "long-sleeve shirt", "short-sleeve shirt", "socks", "belt", "cap", "accessories",
                    "handbook", "tent", "sleeping bag", "sleeping pad", "camping pack", "hiking sticks", "day pack",
                    "scout water bottle", "insect repellent", "compass", "first aid kit", "pillow", "mess kit", "drinking cup",)
scout_store_costs = (60.0, 24.0, 38.0, 27.0, 15.0, 20.0, 25.0, 20.0,
                     24.0, 150.0, 62.5, 27.5, 50.0, 42.5, 35,
                     20.0, 7.5, 12.5, 17.5, 10.0, 15.0, 5.0)
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def boot(path='\\'):
    scout_rpg = ScoutRPG(path)
    if not scout_rpg.filename == "exit":
        scout_rpg.main()


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

    def iter_list(self):
        return ['health', 'hunger', 'thirst', 'money']


class Food:
    def __init__(self, name=None, count=None, fuel=None, duration=None, info=None):
        self.name = name if name else None
        self.count = count if count else None
        self.fuel = fuel if fuel else None
        self.duration = duration if duration else None
        if info:
            self.name = str(info[0])
            self.count = int(info[1])
            self.fuel = int(info[2])
            self.duration = int(info[3])
        else:
            match name:
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

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))


class Drink:
    def __init__(self, name=None, count=None, fuel=None, duration=None, info=None):
        self.name = name if name else None
        self.count = count if count else None
        self.fuel = fuel if fuel else None
        self.duration = duration if duration else None
        if info:
            self.name = str(info[0])
            self.count = int(info[1])
            self.fuel = int(info[2])
            self.duration = int(info[3])
        else:
            match name:
                case 'water':
                    (self.count, self.fuel, self.duration) = (24, 20, 5)
                case 'soda':
                    (self.count, self.fuel, self.duration) = (0, 30, 10)
                case _:
                    (self.count, self.fuel, self.duration) = (0, 0, 0)

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))


class Location:
    def __init__(self, name=None, duration=None, info=None):
        if name and duration:
            self.name = name
            self.duration = int(duration)
        if info:
            (self.name, self.duration) = info
            self.duration = int(self.duration)

    def __repr__(self):
        return self.name + ',' + str(self.duration)


class Chore:
    def __init__(self, name='', cooldown=''):
        self.name = name
        self.cooldown = cooldown


class ScoutRPG:
    def __init__(self, path):
        # Default game setup code, pulled from sonar.py.
        self.new_file = False
        self.filename = ""
        self.path = path
        game_info = bagels.init_game(self, path, 'sct')
        # Default stats for the time being. Health, Hunger, Thirst, and time (date, hour, minute).
        self.capacity = 10
        self.possessions = []
        if game_info:
            # Decrypting everything and cutting off the new line at the end!
            (stats, food, drinks, time, locations) = [Loading.caesar_decrypt(i).split('\n')[0] for i in game_info]
            self.stats = None
            self.food = []
            self.drinks = []
            self.locations = []
            # stats will look something like "100.0\t50\t50\t0"
            try:
                self.stats = Statistics(stats.split('\t'))
                # Food data looks like 5,5,5\t0,10,10\t0,30,35
                for i in food.split('\t'):
                    self.food.append(Food(None, None, None, None, i.split(',')))
                for i in drinks.split('\t'):
                    self.drinks.append(Drink(None, None, None, None, i.split(',')))
                for i in locations_list:
                    self.locations.append(Location('', 0, locations.split('\t')[locations_list.index(i)].split(',')))
                self.time = time.split('\n')[0].split(',')
                self.previous_time = self.time.copy()
                self.difference = [0, 0, 0, 0]
                # Checking for update...
                if -1 in [self.stats.__getattribute__(i) for i in self.stats.iter_list()] or "-1" in self.food.__repr__() or "-1" in self.drinks.__repr__() or "-1" in self.locations.__repr__():
                    raise KeyError
            except (KeyError, IndexError, ValueError):
                # If the element doesn't exist.
                self.update_file()
                Loading.returning("This game was saved in an older version of ScoutRPG. The save file will now be updated.", 3)
                self.quit()

    def quit(self):
        if self.new_file:
            self.filename = input("File name?\n") + '.sct'
        stats = '\t'.join(str(self.stats.__getattribute__(i)) for i in self.stats.iter_list())
        food = '\t'.join(i.__repr__() for i in self.food)
        drinks = '\t'.join(i.__repr__() for i in self.drinks)
        time = ','.join(self.time)
        locations = '\t'.join(i.__repr__() for i in self.locations)
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            for i in (stats, food, drinks, time, locations):
                game.write(Loading.caesar_encrypt(i) + '\n')
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
        return

    def refresh(self, element=None, value=None):
        for i in range(len(self.time)):
            self.time[i] = int(self.time[i])
            self.previous_time[i] = int(self.previous_time[i])
        # Check if we're modifying time or updating it.
        if element and value:
            # Make sure the passed element is ok.
            if 0 <= element <= 4:
                self.time[element] += value
            # Math to calculate total time.
            self.difference[0] += abs(((60 * self.time[3]) + self.time[4]) - ((60 * self.previous_time[3]) + self.previous_time[4]))
            self.difference[1] += abs(((60 * self.time[3]) + self.time[4]) - ((60 * self.previous_time[3]) + self.previous_time[4]))
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
            # Minute rollover
            if self.time[4] >= 60:
                self.time[4] -= 60
                self.time[3] += 1
            # Hour Rollover
            if self.time[3] >= 24:
                self.time[3] -= 24
                self.time[1] += 1
            # Day rollover
            if self.time[1] >= days[self.time[0] - 1]:
                self.time[1] -= days[self.time[0] - 1]
                self.time[0] += 1
            # Month rollover
            if self.time[0] >= 12:
                self.time[0] -= 12
                self.time[2] += 1
            # Updating stats
            for i in self.stats.iter_list():
                if i != "money":
                    self.stats.__setattr__(i, 0.0) if self.stats.__getattribute__(i) < 0.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, 100.0) if self.stats.__getattribute__(i) > 100.0 else self.stats.__getattribute__(i)
        if self.stats.health == 0.0:
            if self.defeat() == 1:
                self.setup()
            else:
                return 1
        for i in range(len(self.time)):
            if self.time[i] < 10:
                self.time[i] = "0" + str(int(self.time[i]))
            else:
                self.time[i] = str(int(self.time[i]))
        self.previous_time = self.time.copy()

    def update_file(self):
        # For every statistic.
        new_stats = Statistics()
        for i in self.stats.iter_list():
            new_stats.__setattr__(i, self.stats.__getattribute__(i) if self.stats.__getattribute__(i) != -1 else new_stats.health)
        self.stats = new_stats

    def main(self):
        # Setup logic
        if self.new_file:
            self.setup()
        while True:
            if self.refresh() == 1:
                return
            # Status report. Date, time, all stats.
            print("\nDate: {}/{}/{}\nTime: {}:{}.".format(self.time[0], self.time[1], self.time[2], self.time[3], self.time[4]))
            print('\n'.join(i + (": $" if i == "Money" else ": ") + str(self.stats.__getattribute__(i.lower())) for i in stats_list))
            action = input('What would you like to do? Type "help" for help').lower()
            if action == "help":
                input('Here is a list of common actions:\n1. Eat\n2. Drink\n3. Sleep\n4. Heal\n5. Chores\n6. Travel\n\n'
                      'You can type "exit" to exit')
            choices = {self.eat: "eat", self.drink: "drink", self.sleep: "sleep", self.heal: "heal",
                       self.chores: "chores", self.travel: "travel"}
            if action in ('quit', 'exit', 'leave', 'save'):
                self.quit()
                return
            for i in choices:
                if action == choices[i]:
                    print()
                    i()
                    break

    def setup(self):
        # input("Welcome to Mars.\nYou and a crew of 5 others traveled here 6 sols agp. A sol is 1 day on Mars, slightly "
        #       "longer than an Earth day. A severe storm struck your landing site and forced your team on an emergency course "
        #       "back to Earth. However, during your trip to the Mars Ascent Vehicle (MAV), a large clump of dirt hit you straight "
        #       "in the chest. You were sucked into the eye of the storm and thrown out the other side. You crew is suddenly "
        #       "hundreds of meters away from you, your chest pains intensely, and your system alarms are going off. Out of shock, "
        #       "your mind slowly drifts away...\nPress ENTER to continue")
        # input("BEEP! BEEP! You recognize that pattern anywhere. Your suit is low on oxygen. You jolt awake, gasping for what "
        #       "little breathable air you have. You get up, familiarize with the surroundings, and beeline to your Martian habitat. "
        #       "You cycle the airlock and head inside.\nPress ENTER to continue.")
        # input("Your head aches, your body feels flat, and your ears are ringing. You are the only one left on the planet, your "
        #       "next rescue attempt is 4 years away, and your equipment and supplements were designed for a 31-sol mission."
        #       "\n\nWelcome to Mars.\nPress ENTER to continue.")
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
        self.locations = [Location(i, 10 * (self.locations.index(i) + 1)) for i in self.locations]
        self.stats = Statistics()
        self.time = ["3", "1", datetime.today().year, "08", "00"]
        self.previous_time = self.time.copy()
        self.difference = [0, 0, 0, 0]
        self.food = [Food(i) for i in ("peanuts", "pancake")]
        self.drinks = [Drink("water")]

    def eat(self):
        print("Here's the food you have:")
        print('\n'.join("{} {} meals".format(str(int(i.count)).title(), i.name) for i in self.food if i.count > 0))
        while True:
            action = input("What would you like to eat?").lower()
            if not action:
                return
            try:
                action = [self.food.index(i) for i in self.food if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                self.food[action].count -= 1
                self.stats.hunger += self.food[action].fuel
                self.refresh(4, self.food[action].duration)
                Loading.returning("You eat a {} meal, and it was {}".format(self.food[action].name.title(), ["tasty", "delicious", "scrumptious"][random.randint(0, 2)]), 2)
                break
            except (IndexError, ValueError):
                Loading.returning("You don't have any {} meals!".format(action) , 2)
        pass

    def drink(self):
        print("Here are the beverages you have:")
        print('\n'.join("{} bottles of {}".format(str(int(i.count)).title(), i.name) for i in self.drinks if i.count > 0))
        while True:
            action = input("What would you like to drink?").lower()
            if not action:
                return
            try:
                action = [self.drinks.index(i) for i in self.drinks if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                self.drinks[action].count -= 1
                self.stats.thirst += self.drinks[action].fuel
                self.refresh(4, self.drinks[action].duration)
                Loading.returning("You drink a bottle of {}, and it was {}".format(self.drinks[action].name.title(), ["quenching", "tasty", "refreshing"][random.randint(0, 2)]), 2)
                break
            except (IndexError, ValueError):
                Loading.returning("You do not have any bottles of {}!".format(action), 2)
        pass

    def sleep(self):
        if int(self.time[3]) >= 21:
            self.refresh(1, 1)
            self.time[3] = "08"
            self.time[4] = "00"
            self.stats.hunger = self.stats.thirst = 25
            print("SLEEP: Until 8:00")
            Loading.returning("It's getting late, so you turn in for the day.", 3)
            Loading.returning("Zzzzzzz...", 3)
        else:
            sleep_time = [0.5, 1, 2, 3, 4][random.randint(0, 4)]
            if self.stats.hunger <= 0 or self.stats.thirst <= 0:
                Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you sleep.", 3)
            match sleep_time:
                case 0.5:
                    self.refresh(4, 30)
                    print("SLEEP: 30 Minutes")
                    Loading.returning("You take a small nap and feel more energized.", 3)
                case 1:
                    self.refresh(3, 1)
                    print("SLEEP: 1 Hour")
                    Loading.returning("You take a good nap and are ready to progress.", 3)
                case 2:
                    self.refresh(3, 2)
                    print("SLEEP: 2 Hours")
                    Loading.returning("You oversleep a little bit, but it's nothing special.", 3)
                case 3:
                    self.refresh(3, 3)
                    print("SLEEP: 3 Hours")
                    Loading.returning("You sleep for a while after your alarm, but you still have time in the day.", 3)
                case 4:
                    self.refresh(3, 4)
                    print("SLEEP: 4 Hours")
                    Loading.returning("Oops! You oversleep a lot and are quite hungry.", 3)

    def heal(self):
        if self.stats.health < 100.0:
            self.stats.health = 100.0
            Loading.returning("You use a small first aid kit, food, and water to replenish yourself.", 3)
            Loading.returning("Make sure to eat and drink regularly!", 2)
        else:
            Loading.returning("You don't need to heal!", 2)

    def chores(self):
        pass

    def travel(self):
        print('\n'.join(str(i.name.title()) + ' --> ' + str(i.duration) + ' minutes' for i in self.locations))
        destination = input("Where would you like to go?").lower()
        destination = destination + " store" if "store" not in destination else destination
        # self.refresh(4, [i.duration for i in self.locations if i.name == destination][0])
        for i in locations_list:
            if destination == i:
                stores = (self.groceries, self.department, self.scout_store)
                self.refresh(4, self.locations[locations_list.index(destination)].duration)
                Loading.progress_bar("Traveling to the {}".format(destination), [i.duration for i in self.locations if i.name == destination][0] / 4)
                stores[locations_list.index(i)]()
                break
        else:
            Loading.returning("Please pick a valid destination.", 2)
        # if destination in ("grocery", "grocery store"):
        #     Loading.progress_bar("Traveling to the grocery store...", )
        #     self.groceries()
        # elif destination in ("department", "department store"):
        #     Loading.progress_bar("Traveling to the department store...", 3)
        #     self.department()
        # elif destination in ("scout", "scout store"):
        #     Loading.progress_bar("Traveling to the scout store...", 3)
        #     self.scout_store()

    def groceries(self):
        print("\n\nWelcome to the grocery store!")
        Loading.returning("Here you can buy food and drinks.", 2)
        print('\nFOOD')
        print('\n'.join(str(food_list.index(food_list[i]) + 1) + '. ' + food_list[i].title() + ' - $' + str(food_costs[i]) + '0' for i in range(len(food_list))))
        print('\nDRINKS')
        print('\n'.join(str(drinks_list.index(drinks_list[i]) + 1) + '. ' + drinks_list[i].title() + ' - $' + str(drinks_cost[i]) + '0' for i in range(len(drinks_list))))
        while True:
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "grocery store"][0] / 4)
                return
            elif buy in food_list:
                if self.buy(buy, self.food, food_list, food_costs) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "grocery store"][0] / 4)
                    break
            elif buy in drinks_list:
                if self.buy(buy, self.drinks, drinks_list, drinks_cost) == 0:
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
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "department store"][0] / 4)
                return
            elif buy in department_list:
                if self.buy(buy, self.possessions, department_list, department_costs) == 0:
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
        print('\nCLOTHING')
        print('\n'.join((str(scout_store_list.index(i) + 1) + '. ' + i.title() + ': $' + str(scout_store_costs[scout_store_list.index(i)]) + '0') for i in scout_store_list[0:7]))
        print('\nOUTDOORS')
        print('\n'.join((str(i - 7) + '. ' + scout_store_list[i].title() + ': $' + str(scout_store_costs[i]) + '0') for i in range(len(scout_store_list))[8:]))
        while True:
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "scout store"][0] / 4)
                return
            elif buy in scout_store_list:
                if self.buy(buy, self.possessions, scout_store_list, scout_store_costs) == 0:
                    Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == "scout store"][0] / 4)
                    break
            else:
                Loading.returning("Please type a valid food/drink.")
    # Buy scouting equipment
        # Scout Pants: $60
        # Scout Shorts: $24
        # Scout Long-sleeve shirt: $38
        # Scout Short-sleeve shirt: $27
        # Scout Socks: $15
        # Scout Belt: $20
        # Scout Cap: $25
        # Scout Uniform accessories: $20

    def buy(self, buy, stat, store_list, store_costs):
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
                if self.stats.money > (quantity * store_costs[store_list.index(buy)]):
                    self.stats.money -= (quantity * store_costs[store_list.index(buy)])
                    try:
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count += quantity
                    except IndexError:
                        stat.append(Food(buy))
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count = quantity
                    print("Purchase successful. Your total was: $" + str(quantity * store_costs[store_list.index(buy)]))
                    if 'yes' in input("Would you like to buy more?").lower():
                        return 1
                    else:
                        # Another 1-liner for loop marvel. It's deprecated but I still love it so I kept it.
                        # length_index = {"grocery store": (food_list, drinks_list), "department store": department_list, "scout store": scout_store_list}
                        # Loading.progress_bar("Traveling back home...", [i.duration for i in self.locations if i.name == [i for i in length_index if store_list in length_index[i]][0]][0] / 4)
                        return 0
                else:
                    Loading.returning("You don't have enough money! ({})".format(self.stats.money), 2)
                    break
            else:
                Loading.returning("Please type a number between 0 and 100.", 2)

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
