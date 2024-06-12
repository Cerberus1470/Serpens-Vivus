"""
Module event_viewer. This module houses the application and a global function.
"""
from System import Loading

time1 = time2 = 0


def update_time(events, index):
    """
    Function to update global variables time1 and time2. Very useful for sorting events based on time.
    :param events: The list of events from the text file.
    :param index: The index to identify which event we are talking about.
    :return: Nothing. Updates global variables.
    """
    global time1, time2
    time1 = (int(events[len(events)-index][12:14]) * 3600) + (int(events[len(events)-index][15:17]) * 60) + int(events[len(events)-index][18:20])
    time2 = (int(events[len(events)-index-1][12:14]) * 3600) + (int(events[len(events)-index-1][15:17]) * 60) + int(events[len(events)-index-1][18:20])


category = "admin"
version = "2.1"
entries = ('event viewer', 'events')


def boot(_):
    """
    This method regulates booting.
    :param _: The unused OS Object, passed due to the iterative nature of the application home screen.
    :return: 4 if the user reset the event log.
    """
    event_viewer = EventViewer(_)
    return EventViewer.main(event_viewer)


class EventViewer:
    """
    Class EventViewer. This class houses the main application.
    """

    def __init__(self, _, page=0):
        self.page = int(page)

    def __repr__(self):
        return "EventViewer(SS1){}".format(self.page)

    def main(self):
        """
        The main application screen.
        :return: 4 if the user reset the event log.
        """
        global time1, time2
        event_log = open('System\\event_log.info', 'r')
        events = list(event_log)
        event_chunks = []
        event_log.close()
        index = 2
        time1 = (int(events[len(events)-1][12:14]) * 3600) + (int(events[len(events)-1][15:17]) * 60) + int(events[len(events)-1][18:20])
        time2 = (int(events[len(events)-index][12:14]) * 3600) + (int(events[len(events)-index][15:17]) * 60) + int(events[len(events)-index][18:20])
        while True:
            try:
                chunk_temp = []
                if index == 2:
                    chunk_temp.append(events[len(events)-1])
                    chunk_temp.append(events[len(events)-2])
                while time1-time2 <= 600:
                    chunk_temp.append(events[len(events)-index - 1])
                    index += 1
                    update_time(events, index)
                index += 1
                update_time(events, index)
                if not chunk_temp:
                    chunk_temp.append(events[len(events) - index + 1])
                event_chunks.append(chunk_temp)
            except IndexError:
                break
        print("This is the event viewer.")
        print("The events are split into chunks based on time. Chunks are split based on 10-minute gaps between events.")
        while True:
            print("\nEVENTS\tPage {} of {}".format(self.page + 1, len(event_chunks)))
            print("Time period: {} to {}".format(event_chunks[self.page][len(event_chunks[self.page]) - 1][1:20], event_chunks[self.page][0][1:20]))
            for j in event_chunks[self.page]:
                print(j, end='')
            choice = Loading.pocs_input('Press [ENTER] or [return] for the next page. Type "prev" for the previous page. Type "exit" to quit. Type "reset" to reset.', self).lower()
            if choice == '':
                if self.page < len(event_chunks)-1:
                    self.page += 1
                continue
            elif choice == 'prev':
                if self.page != 0:
                    self.page -= 1
            elif choice == 'reset':
                if input('Are you sure? Type "RESET" to reset the event log.'):
                    Loading.returning("Resetting event log...", 2)
                    file = open("System\\event_log.info", 'w')
                    file.close()
                    Loading.returning_to_apps()
                    return 4
            else:
                Loading.returning_to_apps()
                return
