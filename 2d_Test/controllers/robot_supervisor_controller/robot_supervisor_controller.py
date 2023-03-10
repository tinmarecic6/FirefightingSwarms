from controller import Supervisor
import random,math

TIME_STEP = 64
green_area = (2,4)
light_intensity_decrement = 0.2
robot_name_constant = "FireRobot"

robot = Supervisor()
root = robot.getRoot()
robots = {}


def get_random_locations():
	y = random.randint(green_area[0],green_area[1])
	x = random.randint(green_area[0],green_area[1])
	while (x,y) in robots.values():
		y = random.randint(green_area[0],green_area[1])
		x = random.randint(green_area[0],green_area[1])
	robot_id = max(robots) + 1 if robots else 1
	robots.update({robot_id:(x,y)})
	return robot_id,x,y


def gen_swarm(swarm_size):
	children = root.getField('children')
	children.importMFNodeFromString(-1, 'DEF ChargingStation ChargingStation { translation 10 10 0.1}')
	children.importMFNodeFromString(-1, 'DEF ChargingStation ChargingStation { translation 10 10 0.1}')
	for _ in range(swarm_size):
		robot_id,x,y = get_random_locations()
		children.importMFNodeFromString(-1,'DEF '+robot_name_constant+str(robot_id)+' SimpleRobot { translation '+str(x)+' '+str(y)+' 0.1 }')


def reduceFire(robotName):
	global fire_changes
	global fire_locations
	fireSeeker = robot.getFromDef(robotName)
	fireSeekerLocation = fireSeeker.getField('translation')
	fireSeekerLocationVector = fireSeekerLocation.getSFVec3f()
	fireSeekerLocationVector2d = [fireSeekerLocationVector[0],fireSeekerLocationVector[1]]
	for idFireLoc, fireLoc in fire_locations.items():
		fireLoc2d = [fireLoc[0],fireLoc[1]]
		distance = math.dist(fireSeekerLocationVector2d, fireLoc2d)
		if distance<2:
			fire_changes[idFireLoc] -= light_intensity_decrement

if __name__ == "__main__":    
	gen_swarm(5)
	while robot.step(TIME_STEP) != -1:
		for bot_id in robots.keys():
			reduceFire(robot_name_constant+str(bot_id))
