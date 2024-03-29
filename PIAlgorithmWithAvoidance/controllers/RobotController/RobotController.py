import math, ast, decimal, time
from controller import Robot

TIME_STEP = 64
robot = Robot()
robot.batterySensorEnable(TIME_STEP)
customData = eval(robot.getCustomData())
group = customData['Group']
leader = customData['Leader']

gps = robot.getDevice('gps')
gps.enable(TIME_STEP)
compass = robot.getDevice('compass')
compass.enable(TIME_STEP)
ls = []
lsNames = ['LeftSensor', 'RightSensor']
for i in range(2):
    ls.append(robot.getDevice(lsNames[i]))
    ls[i].enable(TIME_STEP)
ds = []
dsNames = ['LeftSensorDistance', 'RightSensorDistance']
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
    setSpeed(leftSpeed,rightSpeed)

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

def driveToPoint(point):
    #print(getRobotBearing())
    #print(gps.getValues(),charger)
    # print(getAngle(charger,gps.getValues()),getRobotBearing())
    angleCharging = getAngle(point,gps.getValues())+180
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
    setSpeed(leftSpeed,rightSpeed)
        
    #[int(charger[0]),int(charger[1])]

def setSpeed(left,right):
    leftSensorDistance = ds[0].getValue()
    rightSensorDistance = ds[1].getValue()    
    if leftSensorDistance > rightSensorDistance:
        left = 10
        right = -5
    elif leftSensorDistance < rightSensorDistance:
        left = -5
        right = 10

    wheels[0].setVelocity(left)
    wheels[1].setVelocity(right)
    wheels[2].setVelocity(left)
    wheels[3].setVelocity(right)

def stop():
    wheels[0].setVelocity(0)
    wheels[1].setVelocity(0)
    wheels[2].setVelocity(0)
    wheels[3].setVelocity(0)

def getRelativeLocationBehind(gps,angle):
    theta = math.radians(angle) # angle in radians

    # find the unit vector in the direction of theta
    dx = -math.cos(theta)
    dy = math.sin(theta)

    return (float(gps[0]) - dx*2, float(gps[1]) - dy*2)

def getRelativeLocationLeft(gps,angle):
    theta = math.radians(angle) # angle in radians

    # find the unit vector perpendicular to theta
    dx = -math.sin(theta)
    dy = math.cos(theta)

    return (float(gps[0]) + dx*2, float(gps[1]) - dy*2)

def getRelativeLocationRight(gps,angle):
    theta = math.radians(angle) # angle in radians

    # find the unit vector perpendicular to theta
    dx = -math.sin(theta)
    dy = math.cos(theta)

    return (float(gps[0]) - dx*2, float(gps[1]) + dy*2)

def getRelativeLocation(relativeLocation,gps,angle):
    if relativeLocation == 'behind':
        return getRelativeLocationBehind(gps,angle)
    if relativeLocation == 'left':
        return getRelativeLocationLeft(gps,angle)
    if relativeLocation == 'right':
        return getRelativeLocationRight(gps,angle)
firstDrive = True
comingBackFromCharger = False
while robot.step(TIME_STEP) != -1:
    customData = eval(robot.getCustomData())
    orders = customData['Orders'] # Can be Follow, Charger or FireFight
    if leader:
        target = customData['LeaderTarget']
        #print("behind ",getRelativeLocationBehind(gps.getValues(),(getRobotBearing()+180)%360))
        #print(getRelativeLocationLeft(gps.getValues(),(getRobotBearing()+180)%360))
        #print(getRelativeLocationRight(gps.getValues(),(getRobotBearing()+180)%360))
        leftSensor = ls[0].getValue()
        rightSensor = ls[1].getValue()
        location = customData['LeaderGPS']
        battery = robot.batterySensorGetValue()
        if target != None and len(target) == 2 and leftSensor < 300 and rightSensor < 300 and battery != 1:
            distance = math.sqrt((target[0] - gps.getValues()[0])**2 + (target[1] - gps.getValues()[1])**2)
            if distance < 1:
                print(distance, target, gps.getValues())
                target.append(leftSensor+rightSensor)
                orders = 'FireFight'
                HandleLight(leftSensor, rightSensor)
                location = gps.getValues()
            else:
                driveToPoint(target)
                if firstDrive:
                    location = gps.getValues()
        elif target != None and battery != 1:
            if len(target) == 2:
                print("Lightsensors triggered",distance, target, gps.getValues())
                target.append(leftSensor+rightSensor)
            orders = 'FireFight'
            HandleLight(leftSensor, rightSensor)
            location = gps.getValues()
        elif battery != 1:
            orders = 'FireFight'
            HandleLight(leftSensor, rightSensor)
            location = gps.getValues()
        else:
            target = [gps.getValues()[0],gps.getValues()[1]] 
            driveToPoint(customData["Charger"])
            firstDrive = False
        LeaderJson = """{'Charger': [-10,-10,0.1], 'Leader' : True,'LeaderTarget': """+str(target)+""", 'LeaderGPS' : '"""+str(location)+"""', 'LeaderAngle' : '"""+str((getRobotBearing())%360)+"""', 'Group' : '"""+str(group)+"""', 'Orders' : '"""+orders+"""'}"""
        robot.setCustomData(LeaderJson)
    else:
        if orders == 'Follow' and customData['LeaderGPS'] != None and customData['LeaderAngle'] != None:
            LeaderAngle = float(customData['LeaderAngle'])
            LeaderGPS = [float(i) for i in customData['LeaderGPS'].replace('[','').replace(']','').split(',')]
            relativeLocation = customData['RelativeLocation']
            angle = (getRobotBearing())%360
            goal = getRelativeLocation(relativeLocation,LeaderGPS,LeaderAngle)
            distance = math.sqrt((goal[0] - gps.getValues()[0])**2 + (goal[1] - gps.getValues()[1])**2)
            if distance > 0.4:
                driveToPoint(goal)
            else:
                stop()
        if orders == 'Charger':
            driveToPoint(customData["Charger"])
        if orders == 'FireFight':
            battery = robot.batterySensorGetValue()
            if battery != 1:
                leftSensor = ls[0].getValue()
                rightSensor = ls[1].getValue()
                if comingBackFromCharger == True:
                    LeaderAngle = float(customData['LeaderAngle'])
                    LeaderGPS = [float(i) for i in customData['LeaderGPS'].replace('[','').replace(']','').split(',')]
                    relativeLocation = customData['RelativeLocation']
                    angle = (getRobotBearing())%360
                    goal = getRelativeLocation(relativeLocation,LeaderGPS,LeaderAngle)
                    distance = math.sqrt((goal[0] - gps.getValues()[0])**2 + (goal[1] - gps.getValues()[1])**2)
                    if leftSensor < 300 and rightSensor < 300:
                        comingBackFromCharger = False
                    elif distance > 0.4:
                        driveToPoint(goal)
                    else:
                        comingBackFromCharger = False
                #print(leftSensorDistance,rightSensorDistance)
                HandleLight(leftSensor, rightSensor)
            else:
                comingBackFromCharger = True
                driveToPoint(customData["Charger"])
                