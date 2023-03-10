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

def FindChargingStation():
    print(int(charger[0]))
    print(gps.getValues())
    print(compass.getValues())



while robot.step(TIME_STEP) != -1:
    battery = robot.batterySensorGetValue()
    FindChargingStation()
    if battery != 1:
        leftSensor = ds[0].getValue()
        rightSensor = ds[1].getValue()
        HandleLight(leftSensor, rightSensor)
    else:
        FindChargingStation()