import pygame
import numpy as np
import random
import math
import sys

from scripts.mapInitialization import *

 #Inspiration/tutorial: https://www.youtube.com/watch?v=gKNJKce1p8M
def fps_counter(display):
    font = pygame.font.SysFont("Arial" , 18 , bold = True)
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    display.blit(fps_t,(0,0))


def flatten(xss):
    return [x for xs in xss for x in xs]

def run():
    while True:
        display.fill((200,0,0))


        display.blit(map_display,(0,0))


        for event in pygame.event.get():
                #event is an input of some description
                #CLose window event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        #fps_counter(display)
        #Scale up screen
        screen.blit(pygame.transform.scale(display, screen.get_size()),(0,0))
        pygame.display.update()
        #Force game to run at X FPS
        clock.tick(60)






#========================================================

   # This function allows us to call screen and clock in any future functions containing (self) as an initialisation
pygame.init()

        #Create screen
        #Set windows name
pygame.display.set_caption("Procedural Map")
# resolution of window
x_window = 1400
y_window = 1000

#scale of game. >1 means smaller pixels, <1 means bigger pixels
scale = 0.1


x_res = int(x_window*scale)
y_res = int(y_window*scale)
screen = pygame.display.set_mode((x_window,y_window))

        # To scale up the screen we render at a smaller size then scale it up.
        #Create a black box with 320,240 size.
display = pygame.Surface((x_res,y_res))

        #self.particle = Particle(self,(1,1),)

        #set max FPS
clock = pygame.time.Clock()



#Initialize a large map the size of the display



map = np.zeros([x_res,y_res], dtype=int)


# =============== INITIAL WORLD SETTINGS ================

#tectonic plates - generates a map that is just lines which demonstrate where plates meet.
#This works really well if lines are set as high mountains. undersea mountain ranges are generated!

#Might be interesting to develop volcanos as well?
#(Combine tectonic plate meeting with high mountains or low level sea?)
tectonic_map = tectonic(map)



centre = [int(x_res/2),int(y_res/2)]

for r in range(0,x_res):
     for c in range(0,y_res):
          if np.sqrt((r-centre[0])**2+(c-centre[1])**2) < 25:
               map[r,c] = 6          
#          if c > y_res*0.9:
#               map[r,c] = 7
          if tectonic_map[r,c] == 1:
               map[r,c] = 2

#Initialize any underlying information





tect_display = pygame.surfarray.make_surface(tectonic_map)



"""
0 = declared
1 = mountains
2 = high mountains
3 = plains
4 = forest
5 = water
6 = deep water

"""
#terrain_types [0] is allowed list. [1] is colour
terrain_types =[
    [[1,1,1,1,1,1,1,1],(0,0,0)],      #Undelcared
    [[1,1,1,0,1,0,0,0],(100,100,100)],#Mountains
    [[1,1,1,0,0,0,0,0],(255,255,255)],#High Mountains
    [[1,0,0,1,1,1,0,1],(70,180,30)],  #Plains
    [[1,1,0,1,1,0,0,0],(40,80,30)],   #forest
    [[1,0,0,1,0,1,1,0],(50,60,220)],  #water
    [[1,0,0,0,0,1,1,0],(16,23,100)],  #deep water
    [[1,0,0,1,0,0,0,1],(210,240,50)],  #desert

]


#plt.figure()
#plt.imshow(map, interpolation='none')
#plt.show()

#Constraint satisfaction
map,colour_map = terrainGen(map,tectonic_map,terrain_types)
map_display = pygame.surfarray.make_surface(colour_map)
#create a dictionary of all the maps.

print('terrain generated!')

run()