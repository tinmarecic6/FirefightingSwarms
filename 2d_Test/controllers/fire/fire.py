"""fire controller."""
from controller import Supervisor
import time,random,math,numpy
from collections import Counter

no_lights = 5
fire_square = (0,3)
fire_locations = {}
robot = Supervisor()
root = robot.getRoot()
light_intensity_default = 0.1
light_intensity_increment = 0.01
light_intensity_decrement = 0.2
light_max = 2
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

def get_random_adjecent_location(id):
	#less than 0.5 generates a fire on x axis, greater on y axis
	dist = 0.5
	dir_x_y = numpy.random.uniform()
	dir_more_less = numpy.random.uniform()
	distance = dist if dir_more_less <0.5 else dist*-1
	x,y = fire_locations[id]
	new_x = x+distance if dir_x_y < dist else x
	new_y = y+distance if dir_x_y >= dist else y
	while (new_x,new_y) in fire_locations.values():
		dir_x_y = numpy.random.uniform()
		dir_more_less = numpy.random.uniform()
		distance = dist if dir_more_less <0.5 else dist*-1
		x,y = fire_locations[id]
		new_x = x+distance if dir_x_y < dist else x
		new_y = y+distance if dir_x_y >= dist else y
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
					id,new_x,new_y = get_random_adjecent_location(key)
					children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(new_x)+' '+str(new_y)+' 0.1 attenuation 0 0 5} intensity 0.1')
		# 	print(key,fire_locations[key])
		# print("-----------------")
			
		
if __name__ == '__main__':
	generateFire()

	


