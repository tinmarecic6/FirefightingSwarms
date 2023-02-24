"""fire controller."""
from controller import Supervisor
import time,random

no_lights = 5
fire_square = (0,3)
fire_locations = []


def get_fire_location():
	y = random.randint(fire_square[0],fire_square[1])
	x = random.randint(fire_square[0],fire_square[1])
	while (x,y) in fire_locations:
		y = random.randint(fire_square[0],fire_square[1])
		x = random.randint(fire_square[0],fire_square[1])
	fire_locations.append((x,y))
	return x,y

def generateFire():
	gen_light = True
	light_intensity_default = 0.1
	light_intensity_increment = 0.1
	robot = Supervisor()
	root = robot.getRoot()
	timestep = int(robot.getBasicTimeStep())
	generatedLights = 0
	while robot.step(timestep) != -1:
		children = root.getField('children')
		# children.importMFNodeFromString(-1,'DEF SteenRobot SimpleRobot { translation 0 4 0.1 }')
		# children.importMFNodeFromString(-1,'DEF PointLightFire PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 1}')
		if gen_light == True:
			children.importMFNodeFromString(-1,'DEF PointLightFire1 PointLight { location 1 3 0.3 attenuation 0 0 1 intensity 2}')
			children.importMFNodeFromString(-1,'DEF PointLightFire2 PointLight { location 1 4 0.3 attenuation 0 0 1 intensity 2}')
			gen_light = False
		light_node = robot.getFromDef('PointLightFire1')
		
		light_intensity_field = light_node.getField('intensity')
		light_intensity = light_intensity_field.getSFFloat()
		light_intensity+=light_intensity_increment
		print(light_intensity)
		light_intensity_field.setSFFloat(light_intensity)
		"""
		fire_translation = fire_translation_field.getSFVec3f()
		t = [fire_translation[0], fire_translation[1], fire_translation[2]]
		t[1] = 10000000
		fire_translation_field.setSFVec3f(t)
		"""
		time.sleep(1)
		

if __name__ == '__main__':
	generateFire()

	


