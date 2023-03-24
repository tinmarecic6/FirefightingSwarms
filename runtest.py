import sys
filename = "CurrentOne/worlds/CurrentOne.wbt"

controllerArgs = "controllerArgs"

with open(file=filename,mode="r+") as f:
	lines = f.readlines()
	for line in lines:
		if controllerArgs in line:
			newArgs = controllerArgs + " \"test\""
			print(f"args before = {controllerArgs}")
			lines[lines.index(line)] = newArgs
			print(lines[lines.index(newArgs)])
	print(lines)
	f.writelines(lines)

	# if controllerArgs in line:
	# 	line = controllerArgs + "\"test1\""
	
	# if not line:
	# 	break