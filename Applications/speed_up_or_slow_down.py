from System import Loading


class SpeedSlow:
    category = "utilities"

    @staticmethod
    def boot(os_object):
        SpeedSlow.main()

    @staticmethod
    def main():
        print('Welcome! Default values are 1. Type "help" for more info.')
        speed = fps = f_sec = f_frames = o_sec = o_frames = 1
        while True:
            print('Set clip speed to: {}%'.format(str(speed)))
            print('Type an option to change.\n1. Frames per second = {}\n2. Initial Length (seconds:frames) = {}:{}'
                  '\n3. Final Length = {}:{}\n4. Quit'.format(str(fps), str(o_sec), str(o_frames), str(f_sec), str(f_frames)))
            option = input().lower()
            if option == '':
                print("Please choose an option from the list.")
            elif option in ('1', 'fps', 'frames per second'):
                print('Frames per second?')
                fps = int(input())
                pass
            elif option in ('2', 'initial', 'initial length'):
                print('Initial number of seconds?')
                o_sec = input()
                try:
                    o_frames = int(o_sec.split(':')[1])
                    o_sec = int(o_sec.split(':')[0])
                    pass
                except (ValueError, IndexError):
                    o_sec = int(o_sec)
                    print('Initial number of frames?')
                    o_frames = int(input())
                pass
            elif option in ('3', 'final', 'final length'):
                print('Final number of seconds?')
                f_sec = input()
                try:
                    f_frames = int(f_sec.split(':')[1])
                    f_sec = int(f_sec.split(':')[0])
                    pass
                except (ValueError, IndexError):
                    f_sec = int(f_sec)
                    print('Final number of frames?')
                    f_frames = int(input())
                pass
            elif option in ('4', 'quit'):
                Loading.returning_to_apps()
                return
            elif option == 'help':
                print("1. Frames per second is the number of frames rendered in a given second.\n2. Initial Length (seconds:frames) "
                      "is the length of the clip to be slowed down or sped up, and is given in seconds and frames.\n3. Final "
                      "length is the length of the clip after speeding up or slowing down, also given in seconds and frames.\n"
                      "The clip speed at the top is the speed to set the video clip to.")
            else:
                print("Please choose an option from the list.")

            speed = round((100*((fps*o_sec+o_frames)/(fps*f_sec+f_frames))), 2)
