# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project

from robodk.robolink import *  # API to communicate with RoboDK
from robodk.robomath import *  # basic matrix operations
# Link to RoboDK
# RDK = Robolink()
RDK = Robolink()

# Notify user:
print('To edit this program:\nright click on the Python program, then, select "Edit Python script"')

# Program example:
item = RDK.Item('base')
if item.Valid():
    print('Item selected: ' + item.Name())
    print('Item posistion: ' + repr(item.Pose()))

print('Items in the station:')
itemlist = RDK.ItemList()
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
print(itemlist)

robot.MoveJ([0.000, 0.000, 0.000, -0.000, -90.000, -0.000])
