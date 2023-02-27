"""fire controller."""
from controller import Supervisor
import time,random,math,numpy
from collections import Counter

bounds = (-5,5)
no_lights = 5
fire_square = (-5,5)
fire_locations = {}
robot = Supervisor()
root = robot.getRoot()
light_intensity_default = 0.1
light_intensity_increment = 0.01
light_intensity_decrement = 0.2
light_max = 3
light_threshold = 1
light_gen_chance = 0.001


def add_fire_location(x,y):
	light_id = len(fire_locations)+1
	fire_locations.update({light_id:(x,y)})
	return light_id

def generate_fire_location():
	y = random.randint(fire_square[0],fire_square[1])
	x = random.randint(fire_square[0],fire_square[1])
	while (x,y) in fire_locations.values():
		y = random.randint(fire_square[0],fire_square[1])
		x = random.randint(fire_square[0],fire_square[1])
	light_id = add_fire_location(x,y)
	return light_id,x,y

def get_quadrant(x,y,dir_more_less):
	dist = random.uniform(0.2,0.8)
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
	while (new_x,new_y) in fire_locations.values():
		dir_more_less = numpy.random.uniform()
		new_x, new_y = get_quadrant(x,y,dir_more_less)
	light_id = add_fire_location(new_x,new_y)
	return light_id,new_x,new_y



def generateFire():
	timestep = int(robot.getBasicTimeStep())
	children = root.getField('children')
	children.importMFNodeFromString(-1,'DEF SteenRobot SimpleRobot { translation 0 4 0.1 }')
	for i in range(no_lights):
		id,x,y = generate_fire_location()
		children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 5 intensity 0.1}')
	while robot.step(timestep) != -1:

		# Create a Counter from the dictionary values
		counts = Counter(fire_locations.values())
		# Create a new dictionary with only the keys whose value has a count greater than 1
		result = {k: v for k, v in fire_locations.items() if counts[v] > 1}
		if result:
			print(result)
		for key in list(fire_locations):
			temp_light_node = robot.getFromDef("PointLight"+str(key))
			temp_light_intensity_field = temp_light_node.getField("intensity")
			temp_light_intensity = temp_light_intensity_field.getSFFloat()
			if temp_light_intensity < light_max:
				temp_light_intensity += light_intensity_increment
				temp_light_intensity_field.setSFFloat(temp_light_intensity)
			if temp_light_intensity > light_threshold:
				cur_chance = numpy.random.uniform()
				if cur_chance <= light_gen_chance:
					print("New point")
					id,new_x,new_y = get_random_adjecent_location(key)
					children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(new_x)+' '+str(new_y)+' 0.1 attenuation 0 0 5} intensity 0.1')
		# 	print(key,fire_locations[key])
		# print("-----------------")
			
		
if __name__ == '__main__':
	generateFire()

	


