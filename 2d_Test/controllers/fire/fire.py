"""fire controller."""
from controller import Supervisor
import time,random,math

no_lights = 5
fire_square = (0,3)
fire_locations = {}
robot = Supervisor()
root = robot.getRoot()
light_intensity_default = 0.1
light_intensity_increment = 0.01
light_intensity_decrement = 0.2




def get_fire_location():
	y = random.randint(fire_square[0],fire_square[1])
	x = random.randint(fire_square[0],fire_square[1])
	while (x,y) in fire_locations:
		y = random.randint(fire_square[0],fire_square[1])
		x = random.randint(fire_square[0],fire_square[1])
	light_id = len(fire_locations)+1
	fire_locations[light_id] = (x,y)
	return light_id,x,y

def generateFire():
	timestep = int(robot.getBasicTimeStep())
	generatedLights = 0
	children = root.getField('children')
	children.importMFNodeFromString(-1,'DEF SteenRobot SimpleRobot { translation 0 4 0.1 }')
	for i in range(no_lights):
		id,x,y = get_fire_location()
		children.importMFNodeFromString(-1,'DEF PointLight'+str(id)+' PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 1}')
	while robot.step(timestep) != -1:
		for key, value in fire_locations.items():
			temp_light_node = robot.getFromDef("PointLight"+str(key))
			temp_light_intensity_field = temp_light_node.getField("intensity")
			temp_light_intensity = temp_light_intensity_field.getSFFloat()
			if temp_light_intensity<5:
				temp_light_intensity += light_intensity_increment
				temp_light_intensity_field.setSFFloat(temp_light_intensity)

		"""
		if len(fire_locations) != 0:
			for idFireLoc,fireLoc in enumerate(fire_locations):
				lightNodeTemp = robot.getFromDef('PointLightFire'+str(idFireLoc+1))
				light_intensity_field = lightNodeTemp.getField('intensity')
				light_intensity = light_intensity_field.getSFFloat()
				light_intensity+=light_intensity_increment
				print(light_intensity)
				light_intensity_field.setSFFloat(light_intensity)
		"""
		
if __name__ == '__main__':
	generateFire()

	


