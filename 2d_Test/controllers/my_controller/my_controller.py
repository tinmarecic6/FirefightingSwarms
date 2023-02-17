"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

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
		print(f"{sensor_vals['ls7'] % 6}")
		left_motor.setVelocity(sensor_vals["ls7"] % 6)
		right_motor.setVelocity(sensor_vals["ls0"] % 6)
		# print(high_sensor_val,avg_sensor_vals[sensor_i.getName()])

		# Enter here functions to send actuator commands, like:
		#  motor.setPosition(10.0)
		pass

# Enter here exit cleanup code.
if __name__ == "__main__":    
	# create the Robot instance.
	robot = Robot()
	run_robot(robot)