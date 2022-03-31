class SpeedSlow:
    @staticmethod
    def main():
        print('Welcome! Default values are 1. Type "help" for more info.')
        speed = fps = f_sec = f_frames = o_sec = o_frames = 1
        while True:
            print('Set clip speed to: ' + str(speed) + "%")
            print('Type an option to change.\n1. Frames per second = ' + str(fps) + '\n2. Initial Length (seconds:frames) = ' + str(o_sec) + ':' + str(o_frames) +
                  '\n3. Final Length = ' + str(f_sec) + ':' + str(f_frames) + '\n4. Quit')
            option = input().lower()
            if option == '':
                print("Please choose an option from the list.")
            elif option in ('1', 'fps', 'frames per second'):
                print('Frames per second?')
                fps = int(input())
                pass
            elif option in ('2', 'initial', 'initial length'):
                print('Initial number of seconds?')
                o_sec = int(input())
                print('Initial number of frames?')
                o_frames = int(input())
                pass
            elif option in ('3', 'final', 'final length'):
                print('Final number of seconds?')
                f_sec = int(input())
                print('Final number of frames?')
                f_frames = int(input())
                pass
            elif option in ('4', 'quit'):
                print("Goodbye!")
                break
            elif option == 'help':
                print("1. Frames per second is the number of frames rendered in a given second.\n2. Initial Length (seconds:frames) "
                      "is the length of the clip to be slowed down or sped up, and is given in seconds and frames.\n3. Final "
                      "length is the length of the clip after speeding up or slowing down, also given in seconds and frames.\n"
                      "The clip speed at the top is the speed to set the video clip to.")
            else:
                print("Please choose an option from the list.")

            speed = round((100*((fps*o_sec+o_frames)/(fps*f_sec+f_frames))), 2)
