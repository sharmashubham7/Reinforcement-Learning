import numpy as np
from PIL import Image
import cv2
import pickle


WINSIZE = 10
EXIT_REWARD = 100
FOOD_REWARD = 50
ENEMY_PENALTY =50
MOVE_PENALTY = -2 
LR = 0.1
epsilon = 39.9
ep_decay = 0.999
iterations = 15000
SHOW_EVERY = 1000
DISCOUNT = 0.95
color_dict = {'wal':(100,100,100),
			'agt':(50,150,250),
			'vic':(200,0,9200),
			'enemy':(0,0,200),
			'food':(0,200,0)}




class walls:
	def __init__(self, start = (0,0), alignment = "h", size = 1):
		self.x, self.y = start
		self.size = size
		self.start = start
		self.align = alignment

		if (str(alignment)=="h"):
			self.end = (self.x+size, self.y)
		elif (str(alignment)=="v"):
			self.end = (self.x, self.y+size)

	def __str__(self):
		return f'''object start position: {self.start}, 
		alignment: {self.align} and size {self.size}
		'''

	def __repr__(self):
		return 'Need start-position, alignment and size'




class agent:
	def __init__(self, x = None, y = None):


		if x == None and y == None:
			(x,y) = (np.random.randint(WINSIZE-1), np.random.randint(WINSIZE-1))
			while((x,y) in wallspace):
				(x,y) = (np.random.randint(WINSIZE-1), np.random.randint(WINSIZE-1))

			self.x = x
			self.y = y

		else:
			(_x,_y) = (x,y)
			while((x,y) in wallspace):
				(x,y) = (np.random.randint(WINSIZE-1), np.random.randint(WINSIZE-1))

			self.x = x
			self.y = y



	def action(self, choice):
		if choice == 0:
			self.move(x=1, y=0)
		elif choice == 1:
			self.move(x=-1, y=0)
		elif choice == 2:
			self.move(x=0, y=1)
		elif choice ==3:
			self.move(x=0, y=-1)

	def __sub__(self, other):
		return (self.x - other.x, self.y - other.y)
	def __str__(self):
		return f'x:{self.x} and y:{self.y}'

	def move(self, x=False, y=False):

		_XorY = np.random.randint(-2,2)
		present_x = self.x
		present_y = self.y



		if not x and not y:
			if _XorY >=0 :
				self.x +=np.random.randint(-1,2)
				self.y +=0
			else:
				self.y +=np.random.randint(-1,2)
				self.x +=0


		else:

			self.x +=x
			self.y +=y


		if self.x < 0:
			self.x =0

		elif self.x > WINSIZE-1:
			self.x = WINSIZE-1


		if self.y < 0:
			self.y =0

		elif self.y > WINSIZE-1:
			self.y = WINSIZE-1


		after_move_x = self.x
		after_move_y = self.y


		Flag = False
		if (self.x, self.y) in wallspace:
			Flag = True
			self.x = present_x
			self.y = present_y
		
		# For checking whether agents cross walls.

		cross_flag = False
		if (present_x, present_y) == (0,2) and (self.x,self.y) == (1,1):
			print('trouble')
			print(f'px:{present_x}, py:{present_y}')
			print(f'amx:{after_move_x}, amy:{after_move_y}')
			print(f'lx:{self.x}, ly:{self.y}')

q_table = None

if q_table is None:
	q_table = {}
	for x_diff in range(-WINSIZE+1, WINSIZE):
		for y_diff in range(-WINSIZE+1, WINSIZE):
			q_table[(x_diff, y_diff)]  = [np.random.uniform(-2,0) for i in range(4)]


wallspace = []


w1 = walls((0,0), 'h', 2)
w2 = walls((2,1), 'v' ,3)
wall_lst = [w1,w2]

for i in wall_lst:
	for j in range(i.size):
		if(i.align == 'v'):
			wallspace.append((i.x,i.y+j))
		elif(i.align ==  'h'):
			wallspace.append((i.x+j,i.y))


def main():



	for iteration in range(iterations):

		if iteration % SHOW_EVERY ==0:
			show =True
			print(iteration)
		else:
			show = False

		exit = walls((0,WINSIZE-1), 'h', 1)
		
		agent1 = agent(WINSIZE-1, 0)
		food = agent()
		enemy = agent()

		iteration_score = 0
		food_eaten = False
		for i in range(250):
			obs = agent1 - enemy
			global epsilon
			if np.random.random() > epsilon:
				action_choice = np.argmax(q_table[obs])
			else:
				action_choice = np.random.randint(0, 4)


			agent1.action(action_choice)
			enemy.move()

			new_obs = agent1 - enemy
			max_future_q = np.max(q_table[new_obs])
			current_q = q_table[obs][action_choice]

			if agent1.x == enemy.x and agent1.y == enemy.y:
				score = -ENEMY_PENALTY
				new_q = score


			elif agent1.x == exit.x and agent1.y == exit.y:
				score = EXIT_REWARD
				new_q = score


			
			elif isinstance(food, agent) and agent1.x == food.x and agent1.y == food.y:
			
				score = FOOD_REWARD
				new_q = score
				food = 0
			


			else:
				score = -MOVE_PENALTY
				new_q = (1- LR) * current_q + LR*(score + DISCOUNT * max_future_q)


			q_table[obs][action_choice] = new_q

			if show:



				env = np.zeros((WINSIZE, WINSIZE, 3), dtype = np.uint8)
				if isinstance(food, agent):
					env[food.x][food.y] = color_dict['food']
				env[exit.x][exit.y] = color_dict['vic']				
				env[agent1.x][agent1.y] = color_dict['agt']
				env[enemy.x][enemy.y] = color_dict['enemy']


				def draw_wall(wall):

					if wall.align == 'h':
						for i in range(wall.size):
							env[wall.x+i][wall.y] = color_dict['wal']

					elif wall.align == 'v':
						for i in range(wall.size):
							env[wall.x][wall.y+i] = color_dict['wal']
				
				for i in  wall_lst:
					draw_wall(i)
				env[2][2] = (250,0,0)
				img = Image.fromarray(env, "RGB")
				img = img.resize((300,300))

				cv2.imshow('', np.array(img))

				if score == -ENEMY_PENALTY or score == EXIT_REWARD:
					if cv2.waitKey(500) & 0xFF == ord('q'):
						break

				else:
					if cv2.waitKey(2) & 0xFF == ord('q'):
		
						break

							
			if score == -ENEMY_PENALTY or score == EXIT_REWARD:
				break

		iteration_score += score

		epsilon = epsilon*ep_decay
		if(iteration % 1000 ==0):
			print(f'eps:{epsilon}, iteration:{iteration}')
		



if __name__== "__main__":
	main()

with open(f"q_table.pickle", "wb") as f:
	pickle.dump(q_table, f)
