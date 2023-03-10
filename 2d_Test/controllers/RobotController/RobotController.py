import math
from controller import Robot

TIME_STEP = 64
robot = Robot()
robot.batterySensorEnable(TIME_STEP)
charger = robot.getCustomData().split(',')
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
    bearing = (rad - 1.5708) / math.pi * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0
    return bearing

def cartesianConvertCompassBearingToHeading(heading):
    heading = 360-heading
    heading = heading + 90
    if (heading > 360.0):
        heading = heading - 360.0
    return heading

def cartesianCalcDestinationThetaInDegrees(currentCoordinate, destinationCoordinate):
    return math.atan2(destinationCoordinate[1] - currentCoordinate[1], destinationCoordinate[0] - currentCoordinate[0]) * 180 / math.pi

def cartesianConvertVec3fToCartesianVec2f(coordinate3f):
    return [coordinate3f[0],-coordinate3f[2]]

def cartesianCalcThetaDot(heading, destinationTheta):
    theta_dot = destinationTheta - heading
    if (theta_dot > 180):
        theta_dot = -(360-theta_dot)
    elif (theta_dot < -180):
        theta_dot = (360+theta_dot)
    return theta_dot

def positioningControllerCalcThetaDotToDestination(destinationCoordinate):
	currentCoordinate = cartesianConvertVec3fToCartesianVec2f(gps.getValues())
	robotHeading = cartesianConvertCompassBearingToHeading(getRobotBearing())
	destinationTheta = cartesianCalcDestinationThetaInDegrees(currentCoordinate, destinationCoordinate)
	return cartesianCalcThetaDot(robotHeading, destinationTheta)

def FindChargingStation():
    print(positioningControllerCalcThetaDotToDestination([int(charger[0]),int(charger[1])]))



while robot.step(TIME_STEP) != -1:
    battery = robot.batterySensorGetValue()
    if battery != 1:
        leftSensor = ds[0].getValue()
        rightSensor = ds[1].getValue()
        HandleLight(leftSensor, rightSensor)
    else:
        FindChargingStation()