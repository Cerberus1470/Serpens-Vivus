from System import Loading

time1 = time2 = 0


def update_time(events, index):
    global time1, time2
    time1 = (int(events[len(events)-index][12:14]) * 3600) + (int(events[len(events)-index][15:17]) * 60) + int(events[len(events)-index][18:20])
    time2 = (int(events[len(events)-index-1][12:14]) * 3600) + (int(events[len(events)-index-1][15:17]) * 60) + int(events[len(events)-index-1][18:20])


class EventViewer:
    @staticmethod
    def main():
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
                while time1-time2 <= 600:
                    chunk_temp.append(events[len(events)-index])
                    index += 1
                    update_time(events, index)
                index += 1
                update_time(events, index)
                event_chunks.append(chunk_temp)
            except IndexError:
                break
        print("This is the event viewer.")
        print("The events are split into chunks based on time. Chunks are split based on 10-minute gaps between events.")
        i = 0
        while True:
            print("\nEVENTS\tPage {} of {}".format(i+1, len(event_chunks)-1))
            print("Time period: {} to {}".format(event_chunks[i][len(event_chunks[i])-1][1:20], event_chunks[i][0][1:20]))
            for j in event_chunks[i]:
                print(j, end='')
            choice = input('Press [ENTER] or [return] for the next page. Type "prev" for the previous page. Type "exit" to quit. Type "reset" to reset.').lower()
            if choice == '':
                i += 1
                continue
            elif choice == 'prev':
                if i != 0:
                    i -= 1
            elif choice == 'reset':
                if input('Are you sure? Type "RESET" to reset the event log.'):
                    Loading.returning("Resetting event log...", 2)
                    file = open("System\\event_log.info", 'w')
                    file.close()
            else:
                Loading.returning_to_apps()
                return

