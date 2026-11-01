import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint
import numpy as np
def generateRectangle(cpt):
	for i in range(20):
		fig,ax = plt.subplots(figsize=(0.28,0.28))
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.set_xlim(0, 12)
		ax.set_ylim(0, 12)
		ax.xaxis.set_ticks_position('none')
		ax.yaxis.set_ticks_position('none')
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		# Create a Rectangle patch
		x,y = 0,0
		w = randint(1,10)
		h = randint(1,10)		
		if w < 10 :
			x = randint(1,10-w)
		if h < 10:
			y = randint(1,10-h)
		rect = patches.Rectangle((x,y),w,h,linewidth=1,edgecolor='g',facecolor='none')

		# Add the patch to the Axes
		ax.add_patch(rect)
		plt.savefig('./tests/test'+str(cpt)+'.png')
		plt.close(fig)
		cpt += 1
	return cpt

def generateTriangle(cpt):
	for i in range(20):
		fig,ax = plt.subplots(figsize=(0.28,0.28))
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.set_xlim(0, 12)
		ax.set_ylim(0, 12)
		ax.xaxis.set_ticks_position('none')
		ax.yaxis.set_ticks_position('none')
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		# Create a Rectangle patch
		x = [randint(1,10) for i in range(3)]
		x.append(x[0])
		y = [randint(1,10) for i in range(3)]
		y.append(y[0])
		plt.plot(x, y,'-g')
		plt.savefig('./tests/test'+str(cpt)+'.png')
		plt.close(fig)
		cpt += 1
	return cpt


def generateCircle(cpt):
	for i in range(20):
		r = randint(1,4)
		x = randint(0,5)
		y = randint(0,5)
		circle = plt.Circle((x,y), r, edgecolor='r',facecolor='none')

		fig,ax = plt.subplots(figsize=(0.28,0.28))

		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.set_xlim(-12,12)
		ax.set_ylim(-12,12)
		ax.xaxis.set_ticks_position('none')
		ax.yaxis.set_ticks_position('none')
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		ax.set_aspect(1)
		ax.add_artist(circle)

		plt.savefig('./tests/test'+str(cpt)+'.png')
		plt.close(fig)
		cpt += 1
	return cpt

if __name__ == '__main__':
	cpt = 0
	cpt = generateCircle(cpt)
	cpt = generateRectangle(cpt)
	generateTriangle(cpt)