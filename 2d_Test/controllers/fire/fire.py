"""fire controller."""
from controller import Supervisor
import time,random,math,numpy

no_lights = 5
fire_square = (0,3)
fire_locations = {}
robot = Supervisor()
root = robot.getRoot()
light_intensity_default = 0.1
light_intensity_increment = 0.01
light_intensity_decrement = 0.2
light_max = 6
light_threshold = 3
light_gen_chance = 0.01


def add_fire_location(x,y):
	light_id = len(fire_locations)+1
	fire_locations.update({light_id:(x,y)})
	# fire_locations[light_id] = (x,y)
	return light_id

def generate_fire_location():
	y = random.randint(fire_square[0],fire_square[1])
	x = random.randint(fire_square[0],fire_square[1])
	while (x,y) in fire_locations:
		y = random.randint(fire_square[0],fire_square[1])
		x = random.randint(fire_square[0],fire_square[1])
	light_id = add_fire_location(x,y)
	return light_id,x,y

def get_random_adjecent_location(id):
	#less than 0.5 generates a fire on x axis, greater on y axis
	direction = numpy.random.uniform()
	x,y = fire_locations[id]
	new_x = x+1 if direction < 0.5 else x
	new_y = y+1 if direction >= 0.5 else y
	light_id = add_fire_location(new_x,new_y)
	return light_id,new_x,new_y



def generateFire():
	timestep = int(robot.getBasicTimeStep())
	children = root.getField('children')
	children.importMFNodeFromString(-1,'DEF SteenRobot SimpleRobot { translation 0 4 0.1 }')
	for i in range(no_lights):
		id,x,y = generate_fire_location()
		children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 1}')
	while robot.step(timestep) != -1:
		for key in fire_locations.keys():
			temp_light_node = robot.getFromDef("PointLight"+str(key))
			temp_light_intensity_field = temp_light_node.getField("intensity")
			temp_light_intensity = temp_light_intensity_field.getSFFloat()
			if temp_light_intensity < light_max:
				temp_light_intensity += light_intensity_increment
				temp_light_intensity_field.setSFFloat(temp_light_intensity)
			if temp_light_intensity > light_threshold:
				cur_chance = numpy.random.uniform()
				if cur_chance <= light_gen_chance:
					# print("Would gen a fire now")
					id,new_x,new_y = get_random_adjecent_location(key)
					children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(new_x)+' '+str(new_y)+' 0.1 attenuation 0 0 1}')
				#generate light adjecent to the one already generated with a chance 
			
		
if __name__ == '__main__':
	generateFire()

	


