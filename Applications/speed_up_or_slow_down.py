"""
Module speed_up_or_slow_down. This module contains the app to speed up or slow down clips in video editing.
"""
from System import Loading


class SpeedUpOrSlowDown:
    """
    Class SpeedUpOrSlowDown. Contains the application.
    """
    category = "utilities"

    @staticmethod
    def boot(_):
        """
        This method regulates the startup process for this application.
        :param _: The unused OS Object, passed due to the iterative nature of the application home screen.
        :return: Nothing
        """
        speed_slow = SpeedUpOrSlowDown(_)
        SpeedUpOrSlowDown.main(speed_slow)

    def __init__(self, _, data=None):
        if data is None:
            data = [1, 1, 1]
        self.fps = int(data[0])
        self.f_frames = int(data[1])
        self.o_frames = int(data[2])
        self.speed = round((100 * (self.o_frames / self.f_frames)), 2)

    def __repr__(self):
        return "SpeedUpOrSlowDown(SS1){}(SS2){}(SS2){}".format(self.fps, self.f_frames, self.o_frames)

    def main(self):
        """
        This method is the main application screen.
        :return:
        """
        print('Welcome! Type "help" for more info.')
        # speed = fps = f_sec = f_frames = o_sec = o_frames = 1
        while True:
            try:
                self.speed = round((100 * (self.o_frames / self.f_frames)), 2)
                print('Set clip speed to: {}%'.format(str(self.speed)))
                print('Type an option to change.\n1. Frames per second = {}\n2. Initial Length (seconds:frames) = {}:{}'
                      '\n3. Final Length = {}:{}\n4. Quit'.format(str(self.fps),
                                                                  str(int(self.o_frames / self.fps)), str(self.o_frames - (int(self.o_frames / self.fps) * self.fps)),
                                                                  str(int(self.f_frames / self.fps)), str(self.f_frames - (int(self.f_frames / self.fps) * self.fps))))
                option = Loading.pocs_input("", self).lower()
                if option == '':
                    print("Please choose an option from the list.")
                elif option in ('1', 'fps', 'frames per second'):
                    print('Frames per second?')
                    self.fps = int(input())
                    pass
                elif option in ('2', 'initial', 'initial length'):
                    o_sec = input('Initial number of seconds?')
                    try:
                        self.o_frames = int(o_sec.split(':')[1]) + (int(o_sec.split(':')[0]) * self.fps)
                        pass
                    except (ValueError, IndexError):
                        self.o_frames = int(input('Initial number of frames?')) + (int(o_sec) * self.fps)
                    pass
                elif option in ('3', 'final', 'final length'):
                    f_sec = input('Final number of seconds?')
                    try:
                        self.f_frames = int(f_sec.split(':')[1]) + (int(f_sec.split(':')[0]) * self.fps)
                        pass
                    except (ValueError, IndexError):
                        self.f_frames = int(input('Final number of frames?')) + (int(f_sec) * self.fps)
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
            except (ValueError, IndexError):
                Loading.returning("Incorrect values were entered. Please try again.", 2)
