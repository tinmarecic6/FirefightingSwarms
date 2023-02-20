"""fire controller."""
from controller import Supervisor

robot = Supervisor()

root = robot.getRoot()

epuckNode = robot.getFromDef('e-puck')
children = root.getField('children')

name = robot.getName()
print(name)
children.importMFNodeFromString(-1,'DEF BALL Ball { translation 0 4 1 }')
for i in range(int(children.getCount())):
	child = children.getMFNode(i)
	if child.isProto():
		print(child.getDef())
		print(child.getPosition())



	


