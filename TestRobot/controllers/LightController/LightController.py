from controller import Robot

robot = Robot()
light = robot.getDevice("PointLight")
timestep = int(robot.getBasicTimeStep())
    
while robot.step(timestep) != -1:
    print("Light: "+str(light))
    
    

