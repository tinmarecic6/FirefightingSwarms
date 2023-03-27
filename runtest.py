import sys
controllerArgs = "controllerArgs"

def modify_world_file(filename="CurrentOne/worlds/temp.wbt",args_to_add="none"):
	with open(file=filename,mode="r+") as f:
		lines = f.readlines()
		for line in lines:
			if controllerArgs in line:
				newArgs = controllerArgs +" "+ args_to_add +" \n"
				lines[lines.index(line)] = newArgs
	with open(filename,"w") as f:
		f.writelines(lines)


if __name__ == "__main__":
	no_robots = sys.argv[1]
	light_spawn_chance = sys.argv[2]
	args = f"{no_robots} {light_spawn_chance}"
	modify_world_file(args_to_add=args)
	print(f"{controllerArgs} set to:\nnumber of robots = {no_robots}\nchance of light spawning = {light_spawn_chance}")