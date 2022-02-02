class Jokes:
    def __init__(self):
        return

    def __repr__(self):
        return "< I am a jokes class named " + self.__class__.__name__ + ">"

    @staticmethod
    def main(stats):
        stats["jokes"] = 'running'
        #The original jokes program from Unit 1 of BYU CS Part 1. Takes input and simply prints statements.
        print("What do sprinters eat before a race?")
        input()
        fast = "fast"
        print("Nothing, they " + fast.upper() + "!")
        print()
        print("What concert costs just 45 cents?")
        input()
        nickelback = "nickelback"
        print("50 cent featuring " + nickelback.lower() + "!")
        print()
        print("Why couldn't the bicycle stand up by itself?")
        input()
        two = "two"
        print("It was " + two.upper() + "-tired!")
        input()
        print()
        print("Well, thank you very much for listening to my jokes.", end=' ')
        print("Press [ENTER] or [return] to return to the applications screen!", end=' ')
        input()
