import os
import dynamixel
import sys
import subprocess
import optparse
import yaml
import Tkinter
#import skynet

# Establish a serial connection to the dynamixel network.
serial = dynamixel.SerialStream(port='/dev/ttyUSB0', baudrate=1000000, timeout=1)
# Instantiate our network object
net = dynamixel.DynamixelNetwork(serial)

# Checking for dynamixels with id 1
net.scan(1, 1)
if len(net.get_dynamixels()) > 0:
    print 'There is a dynamixel with ID 1, we will change this id now. Please make sure only 1 dynamixel is connected.'
    new_id = input('Please enter a new id for the dynamixel')
    #changeId(1,new_id) #Changes id from param1 to param2.


print 'Hello! I\'m PR2'

#### Functions that get things done:
# Populate our network with dynamixel objects
def addDynamixel(servoid, initial_position = 512):
    newDynamixel = dynamixel.Dynamixel(servoid, net)
    net._dynamixel_map[servoid] = newDynamixel
    newDynamixel._set_synchronized(False)
    newDynamixel.moving_speed = 200
    newDynamixel.torque_enable = True
    newDynamixel.torque_limit = 600 
    newDynamixel.max_torque = 1023
    newDynamixel.goal_position = initial_position

# Move a servo to a specific position:
def updateDynamixelPosition(servoid, position, maxposition = None, minpositon = None):
    if maxposition is not None:
        if position > maxposition:
            print('Max position reached.')
            return False
    if minpositon is not None:
        if position < minpositon:
            print('Min position reached.')
            return False
    servo = net._dynamixel_map[servoid]
    if abs(servo._get_current_position()-servo._get_goal_position())>40:
        print('Servo is colliding with something. Going to stop motion.')
        if servo._get_current_position()-servo._get_goal_position() > 0:
            servo.goal_position = servo._get_current_position()
        elif servo._get_current_position()-servo._get_goal_position() < 0:
            servo.goal_position = servo._get_current_position()
            
        
    #elif abs(servo._get_current_position()-servo._get_goal_position())>20:
        #print('Servo is moving, waiting to reach final position. Currently at')
    else:
        servo.goal_position = position
        print('Moved servo ' +str(servoid)+ ' to position ' +str(position))

#Get the positon of a servo with its id: 
def getDynamixelPosition(servoid):
    servo = net._dynamixel_map[servoid]
    return servo._get_goal_position()
    net.scan(1, maxid)
    print "Found the following Dynamixels IDs: "
    for dyn in net.get_dynamixels():
        print dyn.id


#### Utility functions, use with care!!
def scanAllIds(maxid = 10):
    # Ping the range of servos that are attached
    print "Scanning for Dynamixels..."
    net.scan(1, maxid)
    print "Found the following Dynamixels IDs: "
    for dyn in net.get_dynamixels():
        print dyn.id
#scanAllIds()
        
#Changes id from param1 to param2.
def changeId(oldid, newid):
    #Make sure to only have 1 dynamixel connected!!
    newDynamixel = dynamixel.Dynamixel(oldid, net)
    net._dynamixel_map[oldid] = newDynamixel
    newDynamixel._set_id(newid)
    #servoId2 = newDynamixel._get_id()
    print 'Success'
#changeId(1,3) #Changes id from param1 to param2.

#Defining servo Id's and adding them to the Dynamixel Network:
wrist_servo_id = 3
claw_servo_id = 2
addDynamixel(wrist_servo_id)
addDynamixel(claw_servo_id)

#Functions when arrow keys are pressed:
def leftKey(event):
    updateDynamixelPosition(wrist_servo_id,getDynamixelPosition(wrist_servo_id)-10,None,190)
    print('Left')
def rightKey(event):
    updateDynamixelPosition(wrist_servo_id,getDynamixelPosition(wrist_servo_id)+10,840)
    print('Right')
def upKey(event):
    updateDynamixelPosition(claw_servo_id,getDynamixelPosition(claw_servo_id)+10,680)
    print('Up')
def downKey(event):
    updateDynamixelPosition(claw_servo_id,getDynamixelPosition(claw_servo_id)-10,None,340)
    print('Down')
def qKey(event):
    print('Bye!')
    main.destroy() #Close Tk window
    sys.exit()

#Initiate Tkinter to allow keyboard input:
main=Tkinter.Tk()
frame=Tkinter.Frame(main, width=100, height= 100)
main.bind('<Left>', leftKey) #When left key is pressed.
main.bind('<Right>', rightKey) #When right key is pressed.
main.bind('<Up>', upKey) #When up key is pressed.
main.bind('<Down>', downKey) #When down key is pressed.
main.bind('<q>', qKey) #When q key is pressed.
frame.pack()
main.mainloop()
