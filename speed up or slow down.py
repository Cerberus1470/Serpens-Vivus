import time
print('Welcome!')
while True:
    print('Frames per second?')
    fps = int(input())
    print('Final number of seconds?')
    f_sec = int(input())
    print('Final number of frames?')
    f_frames = int(input())
    print('Initial number of seconds?')
    o_sec = int(input())
    print('Initial number of frames?')
    o_frames = int(input())
    speed = round((100*((fps*o_sec+o_frames)/(fps*f_sec+f_frames))), 2)
    print('Set clip speed to: ', + speed)
    print('Again?')
    if input().lower().startswith('n'):
        break
