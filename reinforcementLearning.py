import numpy as np
import random

worldMap=np.zeros([6,6])
print(worldMap)

#print(qmap)
cat1Pos = [0,4]
cat2Pos = [3,0]
cheese = ([3,3],[3,4])

print([0,0] in cheese)
print(cheese)

class agent():
	xpos = 0
	ypos = 0
	score = 0

	def movement(x):
		if x == 0 and agent.xpos<5:
			agent.xpos +=1


		elif x == 1 and agent.xpos>0:
			agent.xpos -=1


		elif x == 2 and agent.ypos<5:
			agent.ypos +=1


		elif x == 3 and agent.ypos>0:
			agent.ypos -=1

		else:
			agent.movement(random.randint(0,3))


		return agent.xpos, agent.ypos




for i in range(0,50000):
		
	
	
	x = random.randint(0,3)
	agent.movement(x)
	
	if([agent.xpos,agent.ypos]==cat1Pos or [agent.xpos,agent.ypos]==cat2Pos):
		agent.score -= 100
		
		worldMap[agent.xpos,agent.ypos]+=0.01*agent.score
		#print(worldMap)
		agent.score =0
		agent.xpos = 0
		agent.ypos = 0
		#break


	elif([agent.xpos,agent.ypos] in cheese):
		agent.score +=100
		#print("found cheese")
		worldMap[agent.xpos,agent.ypos]+=0.01*agent.score
		#print(worldMap)
		agent.score =0
		agent.xpos = 0
		agent.ypos = 0
				
		#break
 

	else:
		agent.score -=1

	
		worldMap[agent.xpos][agent.ypos]+=0.01*agent.score
		#print(worldMap)



print(worldMap)
	


p = agent

p.xpos = random.randint(0,5)
p.ypos = random.randint(0,5)


o_xpos = p.xpos
o_ypos = p.ypos
move_stage_1 = []
print("original POS",[p.xpos,p.ypos])
p.movement(0)
print("it went right",[p.xpos,p.ypos])
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos]) 
p.movement(1)
print("did it go left",[p.xpos,p.ypos])
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos])
p.movement(2)
print("did it go up",[p.xpos,p.ypos])
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos])
p.movement(3)
print("did it go down",[p.xpos,p.ypos])

p.xpos = o_xpos
p.ypos = o_ypos
print("*************************************************************************************************************************************************************")



print("original POS",[p.xpos,p.ypos])
p.movement(0)
move_stage_1.append([p.xpos,p.ypos])
print("stage1 move",move_stage_1)
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos])
p.movement(1)
move_stage_1.append([p.xpos,p.ypos])
print("stage1 move",move_stage_1)
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos])
p.movement(2)
move_stage_1.append([p.xpos,p.ypos])
print("stage1 move",move_stage_1)
p.xpos = o_xpos
p.ypos = o_ypos
print("original POS",[p.xpos,p.ypos])
p.movement(3)
move_stage_1.append([p.xpos,p.ypos])
print("stage1 move",move_stage_1)
p.xpos = o_xpos
p.ypos = o_ypos

tmp_lst = []
for e in move_stage_1:
	if e not in tmp_lst:
		tmp_lst.append(e)

move_stage_1 = tmp_lst
print("dskjdhsdhsh",move_stage_1)




print("*************************************************************************************************************************************************************")
