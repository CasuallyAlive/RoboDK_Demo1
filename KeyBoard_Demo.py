# This macro allows moving a robot using the keyboard
# More information about the RoboDK API here:
# https://robodk.com/doc/en/RoboDK-API.html
# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Note: you do not need to keep a copy of this file, your python script is saved with the station
from robodk.robolink import *  # API to communicate with RoboDK
from robodk.robomath import *  # basic matrix operations

RDK = Robolink()

# Arrow keys program example

# get a robot
LEFT_K, RIGHT_K, UP_K, DOWN_K = (None, None, None, None)
robot = RDK.Item('', ITEM_TYPE_ROBOT)
if not robot.Valid():
    print("No robot in the station. Load a robot first, then run this program.")
    pause(5)
    raise Exception("No robot in the station!")

print('Using robot: %s' % robot.Name())
print('Use the arrows (left, right, up, down), Q and A keys to move the robot')
print("Press ESC to exit the program. Pressing 'R' resets the robots position.")
def exit_program(robot):
    robot.MoveJ([0.000, 0.000, 0.000, -0.000, -90.000, -0.000])
    quit()

# define the move increment
move_speed = 10
import sys

stdin_f = None
if os.environ.get('OS', '') == 'Windows_NT':
    import msvcrt as stdin_f
    LEFT_K, RIGHT_K, UP_K, DOWN_K = ([224,75], [224,77], [224,72], [224,80])
else:
    import getch as stdin_f
    LEFT_K, RIGHT_K, UP_K, DOWN_K = ([27,91,68], [27,91,67], [27,91,65], [27,91,66])

while True:
    poll = []
    doesNotRepeat = True
    
    # Validate key down by polling console standard input
    while doesNotRepeat:
        temp = (ord(stdin_f.getch()))
        doesNotRepeat = not temp in poll 
        if(doesNotRepeat):
            poll.append(temp)    
    key = poll
    move_direction = [0, 0, 0]
    # print(key)
    if key == LEFT_K:
        print('arrow left (Y-)')
        move_direction = [0, -1, 0]
    elif key == RIGHT_K:
        print('arrow right (Y+)')
        move_direction = [0, 1, 0]
    elif key == UP_K:
        print('arrow up (X-)')
        move_direction = [-1, 0, 0]
    elif key == DOWN_K:
        print('arrow down (X+)')
        move_direction = [1, 0, 0]
    elif key == [113]:
        print('Q (Z+)')
        move_direction = [0, 0, 1]
    elif key == [114]:
        print('R (reset)')
        robot.MoveJ([0.000, 0.000, 0.000, -0.000, -90.000, -0.000])
    elif key == [97]:
        print('A (Z-)')
        move_direction = [0, 0, -1]
    elif key == [27]:
        print('Exiting Program')
        exit_program(robot=robot)
        break

    # make sure that a movement direction is specified
    if norm(move_direction) <= 0:
        continue

    # calculate the movement in mm according to the movement speed
    xyz_move = mult3(move_direction, move_speed)

    # get the robot joints
    robot_joints = robot.Joints()

    # get the robot position from the joints (calculate forward kinematics)
    robot_position = robot.SolveFK(robot_joints)

    # get the robot configuration (robot joint state)
    robot_config = robot.JointsConfig(robot_joints)

    # calculate the new robot position
    new_robot_position = transl(xyz_move) * robot_position

    # calculate the new robot joints
    new_robot_joints = robot.SolveIK(new_robot_position)
    if len(new_robot_joints.tolist()) < 6:
        print("No robot solution!! The new position is too far, out of reach or close to a singularity")
        continue
    
    # calculate the robot configuration for the new joints
    new_robot_config = robot.JointsConfig(new_robot_joints)

    # Check if we can do a joint movement (check for collisions)
    issues = robot.MoveJ_Test(robot_joints, new_robot_joints)
    if not issues == 0:
        # Skip this point
        print(f"Skipping movement to: {str(new_robot_joints)}. Collision Detected!")
        continue

    # move the robot joints to the new position
    robot.MoveJ(new_robot_joints)
    #robot.MoveL(new_robot_joints)