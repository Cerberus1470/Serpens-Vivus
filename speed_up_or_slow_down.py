class SpeedSlow:
    @staticmethod
    def main():
        print('Welcome! Default values are 1.')
        speed = fps = f_sec = f_frames = o_sec = o_frames = 1
        while True:
            print('Set clip speed to: ' + str(speed) + "%")
            print('Type the number to change.\n1. Frames per second = ' + str(fps) + '\n2. Initial Length (seconds:frames) = ' + str(o_sec) + ':' + str(o_frames) +
                  '\n3. Final Length = ' + str(f_sec) + ':' + str(f_frames) + '\n4. Quit')
            option = int(input())
            if option == 1:
                print('Frames per second?')
                fps = int(input())
                pass
            elif option == 2:
                print('Initial number of seconds?')
                o_sec = int(input())
                print('Initial number of frames?')
                o_frames = int(input())
                pass
            elif option == 3:
                print('Final number of seconds?')
                f_sec = int(input())
                print('Final number of frames?')
                f_frames = int(input())
                pass
            elif option == 4:
                print("Goodbye!")
                break
            else:
                print("Please choose an option from the list.")

            speed = round((100*((fps*o_sec+o_frames)/(fps*f_sec+f_frames))), 2)
