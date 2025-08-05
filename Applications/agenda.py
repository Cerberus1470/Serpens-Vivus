"""
A calendar app with intuitive controls and custom events!
"""

import calendar
import datetime

from System import Loading

category = "utilities"
version = "1.0"
entries = ("calendar", "events", "time", "date", "schedule", "agenda")
event_separator = "(E)"


def boot(os_object=None):
    """
    Used to regulate the bootup sequence for the game
    :param os_object: OS Object passed from Cerberus.
    :return: Nothing
    """
    while True:
        agenda = Agenda(os_object.path.format(os_object.current_user.username))
        agenda.main()
        return


class Event:
    """
    Class Event. Stores all information for a calendar event.
    Title, Date, Time, All-Day, Location, Notes.
    """

    def __init__(self, title: str = "Event", date_time: datetime.datetime = datetime.datetime.now(),
                 all_day: bool = False, location: str = "Nowhere", notes: str = "", info=None):
        if info:
            (self.title, self.date_time, self.all_day, self.location, self.notes) = info
            self.date_time = datetime.datetime.fromisoformat(self.date_time)
            self.all_day = self.all_day == "True"
        else:
            (self.title, self.date_time, self.all_day, self.location, self.notes) = (title, date_time, all_day, location, notes)


class Agenda:
    """
    Class Calendar. Stores all the code for the app.
    """

    def __init__(self, path: str = "\\"):
        self.filename = "{}\\events.cal".format(path)
        try:
            self.file = list(open(self.filename, 'r'))
            self.events = [Event(info=i.split(event_separator)) for i in self.file]
        except FileNotFoundError:
            self.file = open(self.filename, 'x')
            self.events = []
        self.date = datetime.date.today().replace(month=8)
        self.calendar = calendar.TextCalendar(6)

    def __repr__(self):
        return "< I am a Calendar Class with filename: {}>".format(self.file)

    def main(self):
        while True:
            print(" <      {0:%Y}      >\n<< <{space}{0:%B}{space}{extra}> >>".format(self.date, space=" " * int((12 - len('{0:%B}'.format(self.date))) / 2),
                                                                                      extra=" " if len('{0:%B}'.format(self.date)) % 2 == 1 else ""))
            print(self.calendar.formatmonth(self.date.year, self.date.month).split('\n', 1)[1])

            choice = input()
            if choice in ["Y<", "Y>", "M<", "M>"]:
                value = 1 if choice[1] == '>' else -1
                match choice[0]:
                    case "Y":
                        # Year back
                        self.date = self.date.replace(year=self.date.year + value)
                    case "M":
                        try:  # Month back
                            self.date = self.date.replace(month=self.date.month + value)
                        except ValueError:  # Rollover
                            self.date = self.date.replace(year=self.date.year + value, month=self.date.month + value + 12 * (-value))
            elif choice[0] == "M":
                match choice[1:]:
                    case "<<":
                        self.date = self.date.replace(month=1)
                    case ">>":
                        self.date = self.date.replace(month=12)
            elif len(choice.replace("-", "/").replace(".", "/").split("/")) == 3:
                self.date = datetime.date.fromisoformat(self.new_format(choice))
            elif choice in ("exit", "quit", "get me outta here"):
                break
            else:
                Loading.returning("That is not a valid option.", 2)

    @staticmethod
    def new_format(date : str = "1970-01-01"):
        """
        Method to translate different orders of ISO formats to datetime's ISO format.
        :param date: The string provided to convert to datetime's ISO format.
        :return: Proper ISO format to be read by datetime module.
        """
        def add_zero(number: str = "00"):
            """
            Small helper method to add a zero for proper ISO formats.
            :param number: Number.
            :return: Proper number.
            """
            if 1 <= len(number) <= 2:
                return ("0" if len(number) == 1 else "") + number
            else:
                return "00"

        split_date = date.replace("-", "/").replace(".", "/").split("/")
        if len(split_date[0]) == 4:  # First element is the year.
            if 1 <= int(split_date[1]) <= 12:  # Second element is the month.
                return '-'.join([split_date[0], add_zero(split_date[1]), add_zero(split_date[2])])
            else:  # Third element is the month.
                return '-'.join([split_date[0], add_zero(split_date[2]), add_zero(split_date[1])])
        elif len(split_date[1]) == 4:  # Second element is the year.
            if 1 <= int(split_date[0]) <= 12:  # First element is the month.
                return '-'.join([split_date[1], add_zero(split_date[0]), add_zero(split_date[2])])
            else:  # Third element is the month.
                return '-'.join([split_date[1], add_zero(split_date[2]), add_zero(split_date[0])])
        elif len(split_date[2]) == 4:  # Third element is the year.
            if 1 <= int(split_date[0]) <= 12:  # First element is the month.
                return '-'.join([split_date[2], add_zero(split_date[0]), add_zero(split_date[1])])
            else:  # Second element is the month.
                return '-'.join([split_date[2], add_zero(split_date[1]), add_zero(split_date[0])])
        else:
            return None
