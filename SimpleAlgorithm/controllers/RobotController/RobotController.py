import math
from controller import Robot

TIME_STEP = 64
robot = Robot()
robot.batterySensorEnable(TIME_STEP)
charger = list(map(float, robot.getCustomData().split(',')))
gps = robot.getDevice('gps')
gps.enable(TIME_STEP)
compass = robot.getDevice('compass')
compass.enable(TIME_STEP)
ds = []
dsNames = ['LeftSensor', 'RightSensor']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['FrontLeftWheel', 'FrontRightWheel', 'BackLeftWheel', 'BackRightWheel']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

def HandleLight(left, right):
    leftSpeed = -2
    rightSpeed = 2
    if (left == 1000 and right == 1000):
        leftSpeed = 0
        rightSpeed = 0
    elif (left == 1000):
        leftSpeed = 10
        rightSpeed = -5
    elif (right == 1000):
        leftSpeed = -5
        rightSpeed = 10
    elif (left>right):
        leftSpeed = 10
        rightSpeed = 5
    elif (right>left):
        leftSpeed = 5
        rightSpeed = 10
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)

def getRobotBearing():
    north = compass.getValues()
    rad = math.atan2(north[1], north[0])
    angle = math.degrees(rad)+90
    if angle >180:
        angle -= 360
    return angle

def getAngle(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)*-1
    return angle_degrees

def FindChargingStation():
    #print(getRobotBearing())
    #print(gps.getValues(),charger)
    # print(getAngle(charger,gps.getValues()),getRobotBearing())
    angleCharging = getAngle(charger,gps.getValues())+180
    angleRobot = (getRobotBearing()+180)%360
    # print(angleCharging,angleRobot)
    angleDifference = angleCharging - angleRobot
    if angleDifference > 180:
        angleDifference -=360
    # print(angleDifference)
    leftSpeed = 10
    rightSpeed = 10
    if angleDifference > 10:
        leftSpeed = -5
        rightSpeed = 10
    elif angleDifference < -10:
        leftSpeed = 10
        rightSpeed = -5
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
        
    #[int(charger[0]),int(charger[1])]



while robot.step(TIME_STEP) != -1:
    battery = robot.batterySensorGetValue()
    if battery != 1:
        leftSensor = ds[0].getValue()
        rightSensor = ds[1].getValue()
        HandleLight(leftSensor, rightSensor)
    else:
        FindChargingStation()