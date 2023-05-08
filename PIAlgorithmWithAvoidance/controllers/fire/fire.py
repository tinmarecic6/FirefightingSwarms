"""fire controller."""
import datetime
import json
import math
import os
import random
import sys
import time
from collections import Counter

import numpy
import pandas as pd
from controller import Supervisor

"""
General variables
"""
cur_datetime = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
cur_date= datetime.datetime.now().strftime("%d-%m-%Y")
passed_time = 0
simulation_time = 600000
start_time = time.time()
robot = Supervisor()
root = robot.getRoot()
csv_header = ["runID","datetime","algorithm","no_robots","light_generation_chance","formation","time_passed","timestep"]

"""
Fire simulation variables
"""
fire_squares = {
	1:[(9,9),(10,10),(11,11),(12,12),(13,13),(14,14)], #line
	2:[(10,10),(0,-10),(-10,10),(0,10),(4,-5),(7,4)], #spread out
	3:[(-14,0),(-12,-2),(-8,-6),(-6,-10),(-2,-14)], #arch close
	4:[(-14,0),(-12,2),(-8,6),(-6,10),(-2,12),(14,-14)], #line closing off adjecent corner
	5:[(-13,4),(-7,3),(-2,0),(2,-4),(1,-10)], #arch a bit further out
	6:[(-13,4),(-3,3),(7,7),(1,-4),(1,-10)], #arch a bit further out with a single point behind
	7:[(12,12),(-12,12),(12,-12),(10,0),(0,10)] #very spread  out
}
no_lights = 5
fire_square = (0,5)
fire_locations = {}
fire_changes = {}
fire_changes2 = {}
light_intensity_default = 0.1
light_intensity_increment = 0.01
light_intensity_decrement = 0.001
light_max = 2
light_threshold = 1
light_gen_chance = 0.01
num_fires = 0
max_number_of_fire_nodes = 47

"""
Robot simulation variables
"""

timestep = int(robot.getBasicTimeStep())
green_area = (-12,-9)
center_of_arena = -10
group_quadrants = [(-12,-7),(-7,-7),(-9,-12)]
leader_locations = [(-12,-7),(-7,-7),(-7,-12)]
leader_goals = {
	"upper_left" : [-12,12],
	"upper_right" : [12,12],
	"bottom_right" : [12,-12],
	"bottom_left" : [-11,-11]
}
light_intensity_decrement = 0.2
robot_name_constant = "FireRobot"
leader_name_constant = "_leader_"
robots = {}

"""
Charging station variables
"""

charging_station_location = [center_of_arena,center_of_arena,0.1]

"""
Helper functions
"""
def get_distance(a,b):
	distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
	return distance

def double_check(dict_to_check):
	#Check for no fires with the same location
	# Create a Counter from the dictionary values
	counts = Counter(dict_to_check.values())
	# Create a new dictionary with only the keys whose value has a count greater than 1
	result = {k: v for k, v in dict_to_check.items() if counts[v] > 1}
	if result:
		return True
	return False

def get_floor_size(robot):
	floor = robot.getFromDef("RectangularArena")
	floor_size_field = floor.getField("floorSize")
	floor_size = floor_size_field.getSFVec2f()
	return floor_size

def in_arena(x,y,floor_size):
	#x = int
	#y = int
	#floor_size = tuple(a:int,b:int)
	"""
	x needs to be between -a/2,a/2
	y needs to be between -b/2,b/2
	"""
	a,b = floor_size[0],floor_size[1]
	if -a/2 <= x <= a/2 and -b/2 <= y <= b/2:
		return True
	return False

def readArgs():
	with open("args.txt","r") as f:
		lines = f.readlines()
		arguments = lines[0].split(" ")
		return arguments

def check_for_folder(foldername):
	if os.path.exists(f"./runs/{foldername}"):
		return True
	else:
		os.mkdir(f"./runs/{foldername}")

def save_and_exit():
	print("Running  save and exit")
	check_for_folder(f"{cur_date}")
	file_to_save = f"./runs/{cur_date}/run-{cur_datetime}-{run_id}.wbt"
	robot.simulationSetMode("WB_SUPERVISOR_SIMULATION_MODE_PAUSE")
	robot.worldSave(file_to_save)
	robot.simulationQuit(0)


def save_results(filename="AllRunResults.csv",datetime=0,no_robots=0,light_gen_chance=0,formation=0,passed_time=0,timestep=timestep):
	os.chdir("../../../")
	max_index = 0
	datetime = cur_datetime
	if os.path.isfile(filename):
		df = pd.read_csv(filename)
		max_index = df['runID'].max() + 1
	else:
		df = pd.DataFrame(columns = csv_header)
	data = {
		'runID' : int(max_index),
		'datetime': datetime,
		'algorithm': "PIAlgorithmWithAvoidance",
		'no_robots':int(no_robots),
		'light_generation_chance':light_gen_chance,
		'formation':int(formation),
		'time_passed':int(passed_time),
		'timestep':int(timestep)
	  	}
	df.loc[len(df.index)] = data
	df.to_csv(filename,index = False)
	os.chdir("PIAlgorithmWithAvoidance/controllers/fire/")

"""
Fire functions
"""
def add_fire_location(x,y):
	global num_fires
	num_fires = num_fires+1
	fire_locations.update({num_fires:(x,y)})
	return num_fires

def get_random_fire_location():
	y = random.randint(fire_square[0],fire_square[1])
	x = random.randint(fire_square[0],fire_square[1])
	while (x,y) in fire_locations.values():
		y = random.randint(fire_square[0],fire_square[1])
		x = random.randint(fire_square[0],fire_square[1])
	light_id = add_fire_location(x,y)
	return light_id,x,y

def get_quadrant(x,y,dir_more_less):
	dist = random.uniform(1,2)
	if dir_more_less < 0.25:
		new_x = x-dist
		new_y = y+dist
	elif dir_more_less >= 0.25 and dir_more_less < 0.5:
		new_x = x+dist
		new_y = y+dist
	elif dir_more_less >=0.5 and dir_more_less < 0.75:
		new_x = x-dist
		new_y = y-dist
	elif dir_more_less >= 0.75 and dir_more_less <=1:
		new_x = x+dist
		new_y = y-dist
	return new_x,new_y

def get_random_adjecent_location(id):
	dist = 0.5
	dir_more_less = numpy.random.uniform()
	x,y = fire_locations[id]
	new_x, new_y = get_quadrant(x,y,dir_more_less)
	while (new_x,new_y) in fire_locations.values() or not in_arena(new_x,new_y,get_floor_size(robot)):
		dir_more_less = numpy.random.uniform()
		new_x, new_y = get_quadrant(x,y,dir_more_less)
	light_id = add_fire_location(new_x,new_y)
	return light_id,new_x,new_y

def add_fire_changes():
	global fire_changes
	fire_changes = {}
	for key in list(fire_locations):
		fire_changes[key] = light_intensity_increment

def handle_fire_changes():
	global fire_changes,fire_changes2
	toRemoveIds = []
	if fire_changes != fire_changes2:
		fire_changes2 = fire_changes
	for key in list(fire_changes):
		temp_light_node = robot.getFromDef("PointLight"+str(key))
		temp_light_intensity_field = temp_light_node.getField("intensity")
		temp_light_intensity = temp_light_intensity_field.getSFFloat()
		if temp_light_intensity+fire_changes[key]<0:
			toRemoveIds.append(key)
			temp_light_node.remove()
		elif temp_light_intensity + fire_changes[key] < light_max:
			temp_light_intensity += fire_changes[key]
			temp_light_intensity_field.setSFFloat(temp_light_intensity)
	if len(toRemoveIds) != 0:
		[fire_locations.pop(key) for key in toRemoveIds]

def reduceFire(robotName):
	global fire_changes
	global fire_locations
	fireSeeker = robot.getFromDef(robotName)
	fireSeekerBattery = fireSeeker.getField('battery')
	fireSeekerBatteryValue = fireSeekerBattery.getMFFloat(0)
	if fireSeekerBatteryValue > 1:
		fireSeekerLocation = fireSeeker.getField('translation')
		fireSeekerLocationVector = fireSeekerLocation.getSFVec3f()
		fireSeekerLocationVector2d = [fireSeekerLocationVector[0],fireSeekerLocationVector[1]]
		for idFireLoc, fireLoc in fire_locations.items():
			fireLoc2d = [fireLoc[0],fireLoc[1]]
			distance = math.dist(fireSeekerLocationVector2d, fireLoc2d)
			if distance<2:
				fire_changes[idFireLoc] -= light_intensity_decrement
				if fireSeekerBattery.getMFFloat(0) < 2:
					break
				fireSeekerBattery.setMFFloat(0,fireSeekerBatteryValue-1)

def generateFire(random_spread = False,formation_id = 0):
	children = root.getField('children')
	if random_spread:
		for _ in range(no_lights):
			id,x,y = get_random_fire_location()
			children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 5 intensity 0.01}')
	else:
		if formation_id == 0:
			formation_id = random.randrange(1,max(fire_squares))
		current_spread = fire_squares[formation_id]
		for (x,y) in current_spread:
			id = add_fire_location(x,y)
			children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 5 intensity 0.01}')
		print(f"Using formation: {formation_id}")
	simulate_fire(children)

def simulate_fire(children):
	global passed_time
	while robot.step(timestep) != -1:
		update_custom_data()
		check_for_charger()
		if double_check(fire_locations):
			print("Fires generated on the same location!")
		if len(fire_locations) != 0:
			for cur_chance in [numpy.random.uniform() for _ in range(int(len(fire_locations)/5+4))]:
				if cur_chance <= light_gen_chance and len(fire_locations) < max_number_of_fire_nodes:
					key = list(fire_locations)[0]
					if len(fire_locations) != 1:
						key = list(fire_locations)[random.randrange(0,len(fire_locations)-1)]
					temp_light_node = robot.getFromDef("PointLight"+str(key))
					temp_light_intensity_field = temp_light_node.getField("intensity")
					temp_light_intensity = temp_light_intensity_field.getSFFloat()
					if temp_light_intensity > light_threshold:
						id,new_x,new_y = get_random_adjecent_location(key)
						children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(new_x)+' '+str(new_y)+' 0.1 attenuation 0 0 5} intensity 0.1')
		add_fire_changes()
		for bot_id in robots.keys():
			reduceFire(robot_name_constant+str(bot_id))
		handle_fire_changes()

		passed_time += timestep
		if passed_time > simulation_time or not fire_locations:
			save_results(no_robots=no_robots,light_gen_chance=light_gen_chance,formation=formation,passed_time=passed_time,timestep=timestep)
			save_and_exit()
			# robot.simulationSetMode("WB_SUPERVISOR_SIMULATION_MODE_PAUSE")
			break

"""
Robot functions
"""


def get_random_robot_locations():
	y = random.randint(green_area[0],green_area[1])
	x = random.randint(green_area[0],green_area[1])
	while (x,y) in robots.values() and in_arena(x,y,get_floor_size(robot)):
		y = random.randint(green_area[0],green_area[1])
		x = random.randint(green_area[0],green_area[1])
	robot_id = max(robots) + 1 if robots else 1
	robots.update({robot_id:(x,y)})
	return robot_id,x,y



def get_robot_quadrants(points,id):
	group = id%3 + 1
	p = random.choice(points[group])
	x,y = p[0],p[1]
	points[group].remove(p)
	robots.update({str(id):(x,y)})
	return group-1,id,x,y


def gen_all_possible_locations(num_points=50):
	min_disance = 0.5
	x_range = (-11.5,-7)
	y_range = (-11.5,-7)
	quadrants = {1:[],2:[],3:[],4:[]}
	while sum(len(q) for q in quadrants.values()) < num_points:
		x = random.uniform(x_range[0],x_range[1])
		y = random.uniform(y_range[0],y_range[1])
		new_point = (x,y)
		valid = True
		#checking the distance
		for q in quadrants.values():
			for point in q:
				distance = math.sqrt((new_point[0] - point[0])**2 + (new_point[1] - point[1])**2)
				if distance < min_disance:
					valid = False
					break
			if not valid:
				break

		quadrant = None
		if x >= center_of_arena and y >= center_of_arena:
			quadrant = 2
		elif x < center_of_arena and y >= center_of_arena:
			quadrant = 1
		elif x <= center_of_arena and y < center_of_arena:
			quadrant = 3
		elif x >= center_of_arena and y < center_of_arena:
			quadrant = 4
		
		if new_point in leader_locations:
			valid = False
			
		if valid and len(quadrants[quadrant]) < num_points/3:
			quadrants[quadrant].append(new_point)
	#removing quadrant 3 so we dont spawn any robots there and removing quadrant 4 to 3 fo key usage
	quadrants[3] = quadrants.pop(4)
	return quadrants

def check_for_charger():
	for r in robots.keys():
		bot = robot.getFromDef(robot_name_constant+r)
		location  = bot.getField('translation').getSFVec3f()
		dist = get_distance(location,charging_station_location)
		if dist < 5 :
			bot.getField('battery').setMFFloat(0,100)


def update_custom_data():
	for r in robots.keys():
		if leader_name_constant in r:
			leader = robot.getFromDef(robot_name_constant+r)
			leader_custom_data = eval(leader.getField('customData').getSFString())
			LeaderGPS = leader_custom_data["LeaderGPS"]
			LeaderAngle = leader_custom_data["LeaderAngle"]
			leader_order = leader_custom_data["Orders"]
			leader_group = int(leader_custom_data["Group"])
			for follower in robots.keys():
				if leader_name_constant not in follower:
					follower = robot.getFromDef(robot_name_constant+follower)
					follower_custom_data = eval(follower.getField('customData').getSFString())
					follower_group = int(follower_custom_data["Group"])
					if leader_group == follower_group:
						follower_custom_data["LeaderGPS"] = LeaderGPS
						follower_custom_data["LeaderAngle"] = LeaderAngle
						follower_custom_data["Orders"] = leader_order
						follower.getField('customData').setSFString(str(follower_custom_data))


def gen_swarm(no_robots):
	points = gen_all_possible_locations()
	children = root.getField('children')
	children.importMFNodeFromString(-1, 'DEF ChargingStation ChargingStation { translation '+str(charging_station_location[0])+' '+str(charging_station_location[1])+' '+str(charging_station_location[2])+'}')
	for leader_location in enumerate(leader_locations):
		leader_goal = "upper_left" if leader_location[0] % 3 == 0 else "upper_right" if leader_location[0] % 3 == 1 else "bottom_right"
		leader_target = leader_goals[leader_goal]
		print(leader_goal,leader_location[0],leader_location[0]%3)
		LeaderJson = """{'Charger': [-10,-10,0.1], 'Leader' : True, 'LeaderTarget' : """ +str(leader_target)+ """, 'LeaderGPS' : None, 'LeaderAngle' : None, 'Group' : '"""+str(leader_location[0])+"""', 'Orders' : 'Follow'}"""
		robot_id,x,y = leader_location[0],leader_location[1][0],leader_location[1][1]
		children.importMFNodeFromString(-1,'DEF '+robot_name_constant+leader_name_constant+str(robot_id)+' SimpleRobot { translation '+str(x)+' '+str(y)+' 0.1 customData "'+LeaderJson+'"}')
		robots.update({(leader_name_constant+str(robot_id)):(x,y)})
	for id in range(no_robots-len(leader_locations)):
		RelativeLocation = 'behind'
		if id-6 >= 0:
			RelativeLocation = 'right'
		elif id-3 >= 0:
			RelativeLocation = 'left'
		group_id,robot_id,x,y = get_robot_quadrants(points,id)
		FollowerJson = """{'Charger': [-10,-10,0.1], 'Leader' : False, 'LeaderGPS' : None,'LeaderAngle' : None,'RelativeLocation' : '"""+RelativeLocation+"""', 'Group' : '"""+str(group_id)+"""', 'Orders' : 'Follow'}"""
		children.importMFNodeFromString(-1,'DEF '+robot_name_constant+str(robot_id)+' SimpleRobot { translation '+str(x)+' '+str(y)+' 0.1 customData "'+FollowerJson+'"}')
		robots.update({str(robot_id):(x,y)})


if __name__ == "__main__":
	print("Running PIAlgorithmWithAvoidance")
	arguments = readArgs()
	run_id = int(arguments[0])
	no_robots = int(arguments[1])
	light_gen_chance = float(arguments[2])
	formation = int(arguments[3])
	gen_swarm(no_robots=no_robots)
	update_custom_data()
	generateFire(False,formation_id=formation)




