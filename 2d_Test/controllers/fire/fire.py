"""fire controller."""
from controller import Supervisor
import time,random,math

no_lights = 5
fire_square = (0,3)
fire_locations = {}
robot = Supervisor()
root = robot.getRoot()
light_intensity_default = 0.1
light_intensity_increment = 0.1
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
	# children.importMFNodeFromString(-1,'DEF PointLightFire1 PointLight { location 1 3 0.3 attenuation 0 0 1 intensity 2}')
	# children.importMFNodeFromString(-1,'DEF PointLightFire2 PointLight { location 1 4 0.3 attenuation 0 0 1 intensity 2}')
	# light_node = robot.getFromDef('PointLightFire1')
	# light_node2 = robot.getFromDef('PointLightFire2')
	while robot.step(timestep) != -1:
		
		children.importMFNodeFromString(-1,'DEF PointLightFire PointLight { location '+str(x)+' '+str(y)+' 0.1 attenuation 0 0 1}')
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
		"""
		fire_translation = fire_translation_field.getSFVec3f()
		t = [fire_translation[0], fire_translation[1], fire_translation[2]]
		t[1] = 10000000
		fire_translation_field.setSFVec3f(t)
		"""
		#time.sleep(1)



if __name__ == '__main__':
	generateFire()

	


