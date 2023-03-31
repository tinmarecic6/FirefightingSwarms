import sys,os
controllerArgs = "controllerArgs"

def modify_args_file(filename="CurrentOne/Controllers/fire/args.txt",args_to_add="none"):
	with open(file=filename,mode="w") as f:
			f.write(args_to_add)
		

def modify_world_file(filename="CurrentOne/worlds/CurrentOne.wbt",args_to_add="none"):
	with open(file=filename,mode="r+") as f:
		lines = f.readlines()
		for line in lines:
			if controllerArgs in line:
				newArgs = controllerArgs +" "+ args_to_add +"\n"
				lines[lines.index(line)] = newArgs
	with open(filename,"w") as f:
		f.writelines(lines)

def runSim(key,no_robots,light_spawn_chance,formation):
	args = f"{key} {no_robots} {light_spawn_chance} {formation}"
	modify_args_file(args_to_add=args)
	print(f"{controllerArgs} set to:\nnumber of robots = {no_robots}\nchance of light spawning = {light_spawn_chance}\nforamtion id = {formation}")
	os.system("call webots --mode=fast --minimize --no-rendering --stdout --stderr CurrentOne/worlds/CurrentOne.wbt")


if __name__ == "__main__":
	arguments = {
		# 0:[10,0.001,1],
		# 1:[10,0.001,2],
		# 2:[10,0.001,3],
		# 3:[10,0.001,4],
		# 4:[10,0.001,5],
		5:[10,0.001,6],
		6:[10,0.001,7],
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
	for item in arguments.items():	
		# print(item[0],item[1][0],item[1][1],item[1][2])
		runSim(item[0],item[1][0],item[1][1],item[1][2])		
	