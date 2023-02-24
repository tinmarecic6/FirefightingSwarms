from controller import Robot

TIME_STEP = 64
robot = Robot()
print(robot.getName())
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
    leftSpeed = 0
    rightSpeed = 0
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
    
while robot.step(TIME_STEP) != -1:
    leftSensor = ds[0].getValue()
    rightSensor = ds[1].getValue()
    print("left: "+str(leftSensor))
    print("right: "+str(rightSensor))
    HandleLight(leftSensor, rightSensor)
    
    

