import numpy as np
import sys
import random
import pygame
#import flappy_bird_utils
import pygame.surfarray as surfarray
import os, os.path # To count images in directory Too complicatd?
from pygame.locals import *


#Trading on second graph
FPS =240 # Or, may be faster?
SCREENWIDTH  = 13
SCREENHEIGHT = 257
BLUE =  (  0,   0, 255) # for line indicators drawing
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Trader')



#This is a lite version of a program. Only one open order is allowed at a time, fixed size.
class GameState:
    def __init__(self):
	self.money = 1000 # actual money
	self.multiplyer = 100 # 1:100 (Not used in lite version)
	self.orderprice = 0.1 #fixed price for order
	self.order = 0 # -1 :currently sell order 0 : currently no orders 1: currently buy order
	self.order_price = 0 #price at which order was opened
	self.spread = 0.0001 #obviously, spread value
	self.kick_price = 800 # At this balance your game ends
	#path, dirs, files = os.walk("/home/illya/Trader/src/images/specgrams").next()
	#self.max_frames = len(files)
	self.max_frames = 58000 #Just for now
	#self.frame = random.randint(1024, self.max_frames-10000)
	self.frame = 1024
	with open("/home/illya/Trader/src/newvector.txt") as f:
    	    self.prices = map(float, f)

    def frame_step(self, input_actions):
        pygame.event.pump()


	#fd = open('foo.txt','w')
	#old_stdout = sys.stdout   # store the default system handler to be able to restore it
	#sys.stdout = fd

        reward = 0
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: sell
        # input_actions[1] == 1: do nothing
	# input_actions[2] == 1: buy
        if input_actions[0] == 1:
            if self.order == 0: #Making sell order
		self.order = -1
		self.order_price = self.prices[self.frame]
	    if self.order == 1: #Closing buy order
		buf = 1000 * self.orderprice * self.multiplyer *(self.prices[self.frame] - self.order_price -  self.spread) # Income/ Loss
		self.money += buf  
		self.order = 0
    		f1=open('./testfile', 'a')
		f1.write("Buy: Gain: {0:.3f};\n".format(buf))
		f1.close
		self.order_price = 0
		if buf > 0:
			reward = 0.5 # Got money
		if buf < 0:
			reward = -0.5# Lost money

        if input_actions[2] == 1:
            if self.order == 0: #Making buy order
		self.order = 1
		self.order_price = self.prices[self.frame]
	    if self.order == -1: # Closing sell order
		buf = 1000 * self.orderprice * self.multiplyer * ( self.order_price - self.prices[self.frame] - self.spread) # Income/ Loss
		self.money += buf  
		self.order = 0
    		f1=open('./testfile', 'a')
		f1.write("Sell: Gain: {0:.3f};\n".format( buf))
		self.order_price = 0
		f1.close
		if buf > 0:
			reward = 0.5 # Got money
		if buf < 0:
			reward = -0.5# Lost money


        # check if game ended  - out of money ! or pictures ended
	buf = 0 # In case no order is held
	if self.order == 1:
	    buf = 1000 * self.order_price* self.multiplyer * ( self.prices[self.frame] - self.order_price - self.spread)
	if self.order == -1:
	    buf = 1000 * self.order_price* self.multiplyer * ( self.order_price - self.prices[self.frame] - self.spread)

	#Need an exception when have not enough values!!!(self.prices)
	#Leaving game if no money or no more frames
	buff = self.money + buf
        isCrash= (buff < self.kick_price) 

	isOutOfFrames = (self.frame + 2 > self.max_frames)

        if isCrash:
            terminal = True
            self.__init__()
	    reward = -1
	    #If we've ran out of frames, it's not networks fault

	if isOutOfFrames:
	    buf1 = self.money
	    terminal = True
	    self.__init__()
	    self.money = buf1

        # draw images
	IMAGE_PATH = '/home/illya/Trader/src/newspecgrams/img' + str(self.frame) + '.png'
	current_screen = pygame.image.load(IMAGE_PATH).convert()
        SCREEN.blit(current_screen, (0,0)) # draws one image over another

        showState(self)

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())

	#Updating
        pygame.display.update() # Do we need it?
        #print ("FPS" , FPSCLOCK.get_fps())
	FPSCLOCK.tick(FPS)
	self.frame += 1
	ac = self.money

	#fd.close()
        return image_data, reward, terminal, ac # did this to know, what's the progress



#Need to be calibrated - so doesn't overlay needed information
#Now this function also tells player the state he is ight now by colour line in low pixel row
#And doesn't tell money anymore - at this size it won't be seen either way
def showState(self):

    if self.order == -1: #green indicator
	pygame.draw.line(SCREEN, GREEN, [0, 256], [12, 256], 1) #Numeration from 0, so...
    if self.order == 0: # red indicator
	pygame.draw.line(SCREEN, RED, [0, 256], [12, 256], 1)
    if self.order == 1: # blue indicator
	pygame.draw.line(SCREEN, BLUE, [0, 256], [12, 256], 1)
	
    #score = 'Frame: ' +str(self.frame)+  ' Money: ' + str(self.money) + ' Current order: ' + buf
    #label = myfont.render(score, 1, (0,0,0))
    #SCREEN.blit(label, (10, 10))

#Implemented so the network can see in which state it is right now












