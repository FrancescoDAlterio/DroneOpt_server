
import time

drone_is_moving = False;

def execute_movement(type=None,distance=None,heigh=None):

    global drone_is_moving

    drone_is_moving = True;
    print " DroneControl: drone is moving:",drone_is_moving
    print "DroneControl: Drone computes",type," movement. distance:",distance,", heigh:",heigh
    time.sleep(3)
    drone_is_moving = False;
    print "DroneControl: Drone stops"

