from Applications import bagels
from System import Loading
from datetime import datetime
import random


def boot(path='\\'):
    scout_rpg = ScoutRPG(path)
    if not scout_rpg.filename == "exit":
        scout_rpg.main()


class Food:
    def __init__(self, name='', info=None):
        self.name = name
        if info:
            self.count = int(info[0])
            self.fuel = int(info[1])
            self.duration = int(info[2])
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
        return ','.join(str(x) for x in (self.count, self.fuel, self.duration))


class Drink:
    def __init__(self, name='', info=None):
        self.name = name
        if info:
            self.count = int(info[0])
            self.fuel = int(info[1])
            self.duration = int(info[2])
        else:
            self.drinks = {"water": [24, 20, 5], "soda": [0, 30, 10]}
            match name:
                case 'water':
                    (self.count, self.fuel, self.duration) = (24, 20, 5)
                case 'soda':
                    (self.count, self.fuel, self.duration) = (0, 30, 10)
                case _:
                    (self.count, self.fuel, self.duration) = (0, 0, 0)

    def __repr__(self):
        return ','.join(str(x) for x in (self.count, self.fuel, self.duration))


class ScoutRPG:
    food = ("peanuts", "breakfast burrito", "pancake", "mac and cheese", "tofu teriyaki")
    drinks = ("water", "soda")
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, path):
        # Default game setup code, pulled from sonar.py.
        self.new_file = False
        self.filename = ""
        self.path = path
        game_info = bagels.init_game(self, path, 'spc')
        # Default stats for the time being. Health, Hunger, Thirst, and time (sol, hour, minute).
        if game_info:
            # Coming later, after we define everything we need to use to play.
            (stats, food, drinks, time) = game_info
            self.stats = {}
            self.food = []
            self.drinks = []
            # stats will look something like "100,50,50"
            for i in ("Health", "Hunger", "Thirst"):
                self.stats[i] = float(Loading.caesar_decrypt(stats).split('\n')[0].split(',')[("Health", "Hunger", "Thirst").index(i)])
            # Food data looks like 5,5,5\t0,10,10\t0,30.
            for i in ScoutRPG.food:
                self.food.append(Food(i, Loading.caesar_decrypt(food).split('\n')[0].split('\t')[ScoutRPG.food.index(i)].split(',')))
            for i in ScoutRPG.drinks:
                self.drinks.append(Drink(i, Loading.caesar_decrypt(drinks).split('\n')[0].split('\t')[ScoutRPG.drinks.index(i)].split(',')))
            self.time = Loading.caesar_decrypt(time).split('\n')[0].split(',')
            self.previous_time = self.time.copy()
            self.difference = [0, 0, 0, 0]
            pass

    def main(self):
        # Setup logic
        if self.new_file:
            self.setup()
        while True:
            self.update()
            # Status report. Date, time, all stats.
            print("Date: {}/{}/{}\nTime: {}:{}.".format(self.time[0], self.time[1], self.time[2], self.time[3], self.time[4]))
            for i in self.stats:
                print(str(i) + ": " + str(self.stats[i]))
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
            input("Welcome to Scouting!\nYou have embarked on a journey far beyond any other. Your skills will be tested, both "
                  "mentally and physically. Your memory will be trained. Your survival instinct will be brought to life.\nPress ENTER "
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
        self.stats = {"Health": 100, "Hunger": 50, "Thirst": 50}
        self.time = ["3", "1", datetime.today().year, "08", "00"]
        self.previous_time = self.time.copy()
        self.difference = [0, 0, 0, 0]
        self.food = [Food(i) for i in ScoutRPG.food]
        self.drinks = [Drink(i) for i in ScoutRPG.drinks]

    def quit(self):
        if self.new_file:
            self.filename = input("File name?\n") + '.spc'
        stats = ','.join(str(self.stats[i]) for i in self.stats)
        food = '\t'.join(i.__repr__() for i in self.food)
        drinks = '\t'.join(i.__repr__() for i in self.drinks)
        time = ','.join(self.time)
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            game.write(Loading.caesar_encrypt(stats) + '\n')
            game.write(Loading.caesar_encrypt(food) + '\n')
            game.write(Loading.caesar_encrypt(drinks) + '\n')
            game.write(Loading.caesar_encrypt(time) + '\n')
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
        return

    def update(self, element=None, value=None):
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
                self.stats["Hunger"] -= 5 * (self.difference[0] / 60)
                self.difference[0] = 0
            if self.difference[1] >= 30:
                self.stats["Thirst"] -= 5 * (self.difference[1] / 30)
                self.difference[1] = 0
            if self.stats["Hunger"] <= 0:
                self.difference[2] += (60 * (abs(self.stats["Hunger"]) / 5))
            if self.stats["Thirst"] <= 0:
                self.difference[3] += (30 * (abs(self.stats["Thirst"]) / 5))
            if self.stats["Hunger"] <= 0 and self.difference[2] >= 10:
                self.stats["Health"] -= 1 * (self.difference[2] / 10)
                self.difference[2] = 0
            if self.stats["Thirst"] <= 0 and self.difference[3] >= 5:
                self.stats["Health"] -= 1 * (self.difference[3] / 5)
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
            if self.time[1] >= ScoutRPG.days[self.time[0] - 1]:
                self.time[1] -= ScoutRPG.days[self.time[0] - 1]
                self.time[0] += 1
            # Month rollover
            if self.time[0] >= 12:
                self.time[0] -= 12
                self.time[2] += 1
            # Updating stats
            for i in self.stats:
                self.stats[i] = 0 if self.stats[i] < 0 else self.stats[i]
                self.stats[i] = 100 if self.stats[i] > 100 else self.stats[i]
        for i in range(len(self.time)):
            if self.time[i] < 10:
                self.time[i] = "0" + str(int(self.time[i]))
            else:
                self.time[i] = str(int(self.time[i]))
        self.previous_time = self.time.copy()

    def eat(self):
        print("Here's the food you have:")
        print('\n'.join("{} {} meals".format(str(int(i.count)).capitalize(), i.name) for i in self.food if i.count > 0))
        while True:
            try:
                action = ScoutRPG.food.index(input("What would you like to eat?").lower())
                if self.food[action].count <= 0:
                    Loading.returning("You don't have any {} meals!".format(action))
                    continue
                # Correctly remove 1, add hunger, and add time.
                self.food[action].count -= 1
                self.stats["Hunger"] += self.food[action].fuel
                self.update(4, self.food[action].duration)
                Loading.returning("You eat a {} meal, and it was {}".format(action, ["tasty", "delicious", "scrumptious"][random.randint(0, 2)]), 2)
                break
            except (IndexError, ValueError):
                Loading.returning("Please pick a valid food.", 2)
        pass

    def drink(self):
        print("Here are the beverages you have:")
        print('\n'.join("{} bottles of {}".format(str(int(i.count)).capitalize(), i.name) for i in self.drinks if i.count > 0))
        while True:
            try:
                action = ScoutRPG.drinks.index(input("What would you like to drink?").lower())
                if self.drinks[action].count <= 0:
                    Loading.returning("You don't have any bottles of {}!".format(action))
                    continue
                # Correctly remove 1, add hunger, and add time.
                self.drinks[action].count -= 1
                self.stats["Thirst"] += self.drinks[action].fuel
                self.update(4, self.drinks[action].duration)
                Loading.returning("You drink a bottle of {}, and it was {}".format(ScoutRPG.drinks[action], ["quenching", "tasty", "refreshing"][random.randint(0, 2)]), 2)
                break
            except (IndexError, ValueError):
                Loading.returning("Please pick a valid drink.", 2)
        pass

    def sleep(self):
        if int(self.time[3]) >= 21:
            self.update(1, 1)
            self.time[3] = "08"
            self.time[4] = "00"
            self.stats["Hunger"] = self.stats["Thirst"] = 25
            print("SLEEP: Until 8:00")
            Loading.returning("It's getting late, so you turn in for the day.", 3)
            Loading.returning("Zzzzzzz...", 3)
        else:
            sleep_time = [0.5, 1, 2, 3, 4][random.randint(0, 4)]
            if self.stats["Hunger"] <= 0 or self.stats["Thirst"] <= 0:
                Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you sleep.", 3)
            match sleep_time:
                case 0.5:
                    self.update(4, 30)
                    print("SLEEP: 30 Minutes")
                    Loading.returning("You take a small nap and feel more energized.", 3)
                case 1:
                    self.update(3, 1)
                    print("SLEEP: 1 Hour")
                    Loading.returning("You take a good nap and are ready to progress.", 3)
                case 2:
                    self.update(3, 2)
                    print("SLEEP: 2 Hours")
                    Loading.returning("You oversleep a little bit, but it's nothing special.", 3)
                case 3:
                    self.update(3, 3)
                    print("SLEEP: 3 Hours")
                    Loading.returning("You sleep for a while after your alarm, but you still have time in the day.", 3)
                case 4:
                    self.update(3, 4)
                    print("SLEEP: 4 Hours")
                    Loading.returning("Oops! You oversleep a lot and are quite hungry.", 3)

    def heal(self):
        pass

    def travel(self):
        pass

    def chores(self):
        pass
