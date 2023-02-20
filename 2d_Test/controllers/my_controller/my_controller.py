"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

light_threshold = 3000
def run_robot(robot):
	
	timestep = int(robot.getBasicTimeStep())

	#motors
	left_motor = robot.getDevice("left wheel motor")
	right_motor = robot.getDevice("right wheel motor")

	left_motor.setPosition(float("inf"))
	right_motor.setPosition(float("inf"))

	left_motor.setVelocity(0)
	right_motor.setVelocity(0)
	#sensors
	left_sensors = ["ls1,ls2,ls3"]
	right_sensors = ["ls4,ls5,ls6"]
	light_sensors = []

	
	light_sensors.append(robot.getDevice("ls0"))
	light_sensors.append(robot.getDevice("ls7"))
	light_sensors[0].enable(timestep)
	light_sensors[1].enable(timestep)
	
	while robot.step(timestep) != -1:
		# Process sensor data here.
		sensor_vals = {"ls0":0,"ls7":0}

		for sensor_i in light_sensors:
			temp_sensor_val = sensor_i.getValue()
			sensor_vals[sensor_i.getName()] = temp_sensor_val
		# print(f"sensor 7:{sensor_vals['ls7']}")
		# print(f"sensor 0:{sensor_vals['ls0']}")
		if sensor_vals["ls7"] > sensor_vals["ls0"]:
			left_motor.setVelocity(3)
			right_motor.setVelocity(1)
		elif sensor_vals["ls0"] > sensor_vals["ls7"]:
			left_motor.setVelocity(1)
			right_motor.setVelocity(3)
		else:
			left_motor.setVelocity(5)
			right_motor.setVelocity(5)
		if sensor_vals["ls0"] < 100:
			left_motor.setVelocity(0)
			right_motor.setVelocity(0)
			
		pass

# Enter here exit cleanup code.
if __name__ == "__main__":    
	# create the Robot instance.
	robot = Robot()
	run_robot(robot)