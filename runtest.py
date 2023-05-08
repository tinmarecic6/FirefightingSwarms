import os
controllerArgs = "controllerArgs"

simple_algorithm = {"world":"SimpleAlgorithm/worlds/SimpleAlgorithm.wbt","args":"SimpleAlgorithm/controllers/fire/args.txt"}
simple_algorithm_with_avoidance = {"world":"SimpleAlgorithmWithAvoidance/worlds/SimpleAlgorithmWithAvoidance.wbt", "args":"SimpleAlgorithmWithAvoidance/controllers/fire/args.txt"}
pi_algorithm = {"world":"PIAlgorithm/worlds/PIAlgorithm.wbt","args":"PIAlgorithm/controllers/fire/args.txt"}
pi_algorithm_with_avoidance = {"world":"PIAlgorithmWithAvoidance/worlds/PIAlgorithmWithAvoidance.wbt","args":"PIAlgorithmWithAvoidance/controllers/fire/args.txt"}


algorithms = [
		# simple_algorithm,
		# simple_algorithm_with_avoidance,
		pi_algorithm,
		pi_algorithm_with_avoidance]

def modify_args_file(filename,args_to_add="none"):
	with open(file=filename,mode="w") as f:
			f.write(args_to_add)
		

def runSim(algorithm,key,no_robots,light_spawn_chance,formation):
	args = f"{key} {no_robots} {light_spawn_chance} {formation}"
	modify_args_file(filename=algorithm["args"] ,args_to_add=args)
	print(f"Using algorithm: {algorithm['world']}\n {controllerArgs} set to:\nnumber of robots = {no_robots}\nchance of light spawning = {light_spawn_chance}\nforamtion id = {formation}")
	os.system("call webots --mode=fast --minimize --no-rendering --stdout "+algorithm["world"])


if __name__ == "__main__":
	arguments = {
		0:[10,0.001,1],
		1:[10,0.001,2],
		# 2:[10,0.001,3],
		# 3:[10,0.001,4],
		# 4:[10,0.001,5],
		# 5:[10,0.001,6],
		# 6:[10,0.001,7],
		# 7:[10,0.005,1],
		# 8:[10,0.005,2],
		# 9:[10,0.005,3],
		# 10:[10,0.005,4],
		# 11:[10,0.005,5],
		# 12:[10,0.005,6],
		# 13:[10,0.005,7],
		# 14:[10,0.01,1],
		# 15:[10,0.01,2],
		# 16:[10,0.01,3],
		# 17:[10,0.01,4],
		# 18:[10,0.01,5],
		# 19:[10,0.01,6],
		# 20:[10,0.01,7]
		}
	
for alg in algorithms:
	for _ in range(1):
		for item in arguments.items():	
			runSim(alg,item[0],item[1][0],item[1][1],item[1][2])		
	