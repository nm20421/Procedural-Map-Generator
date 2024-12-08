import numpy as np
import random as rd
import matplotlib.pyplot as plt
import pygame


def tectonic(map):
    #creat tectonic plates. These determine where most mountains will be. (and volcanos)
    map_size = [np.size(map,0),np.size(map,1)]
    tectonic_map = np.zeros(map_size)

    #number of tectonic plates.
    n_plates = 2

    #Uses straight lines currently but using something like voroni tessalation might be interesting.
    #would need to work out how to wrap it but show be possible

    for plate in range(0,n_plates):
        #choose two random points on edge of map. the points cannot be on the same side.
        p1 = [0,0]
        #p1 - sides or top/bottom
        t_rand = rd.random()
        if t_rand <= 0.25: #top
            loc_1 = 0
        elif t_rand <= 0.5: # bottom
            loc_1 = 1 
        elif t_rand <= 0.75: #left
            loc_1 = 2
        else:                #right
            loc_1 = 3 

        if loc_1 <= 1:
            p1[1] = rd.randint(0,map_size[1]-1)
            if loc_1 == 0:
                p1[0] = 0
            else:
                p1[0] = map_size[0]-1


        else:
            p1[0] = rd.randint(0,map_size[0]-1)
            if loc_1 == 2:
                p1[1] = 0
            else:
                p1[1] = map_size[1]-1



        p2 = [0,0]
        loc_2 = loc_1
        #p2 - sides or top/bottom
        while loc_2 == loc_1:
            t_rand = rd.random()
            if t_rand <= 0.25: #top
                loc_2 = 0
            elif t_rand <= 0.5: # bottom
                loc_2 = 1 
            elif t_rand <= 0.75: #left
                loc_2 = 2
            else:                #right
                loc_2 = 3 

        if loc_2 <= 1:
            p2[1] = rd.randint(0,map_size[1]-1)
            if loc_2 == 0:
                p2[0] = 0
            else:
                p2[0] = map_size[0]-1


        else:
            p2[0] = rd.randint(0,map_size[0]-1)
            if loc_2 == 2:
                p2[1] = 0
            else:
                p2[1] = map_size[1]-1


        #find line equations.
        gradient = (p1[0]-p2[0])/(p1[1]-p2[1])
        c = p1[0] - gradient*p1[1]

        #find longest side:
        dy = abs(p1[0]-p2[0])
        dx = abs(p1[1]-p2[1])

        if dx > dy: #more x values (COLUMNS)
            x_vals = np.linspace(p1[1],p2[1],dx+1)
            y_vals = gradient*x_vals + c

        if dy > dx:
            y_vals = np.linspace(p1[0],p2[0],dy+1)
            x_vals = (y_vals-c)/gradient
        
        for point in range(0,len(x_vals)):
            tectonic_map[int(y_vals[point]),int(x_vals[point])] = 1

    return tectonic_map






def checkConflicts(r,c,map,tile,terrain_types):

    map_size = [np.size(map,0),np.size(map,1)]

    #tile = map[r,c]
    conflicts = 0

    range_c = 2

    for dr in range(-range_c,range_c+1):
        for dc in range(-range_c,range_c+1):
            tr = (r+dr+map_size[0])%map_size[0]
            tc = (c+dc+map_size[1])%map_size[1]
            test_tile = map[tr,tc]

            if terrain_types[tile][0][test_tile] == 0:
                conflicts += 1


    return conflicts





def leastConflicts(map,tectonic_map,terrain_types):
    success = True
    
    map_size = [np.size(map,0),np.size(map,1)]
    n_terrains = len(terrain_types)

    n_locations = np.size(map)
    n_tests = 15

    for location in range(0,n_locations):
        r = rd.randint(0,map_size[0]-1)  
        c = rd.randint(0,map_size[1]-1)  
        conflicts = checkConflicts(r,c,map,map[r,c],terrain_types)

        if conflicts > 0 or map[r,c] == 0:
            success = False
            #pick new terrain type
            best_type = 0
            leastConflicts = 100
            for test in range(0,n_tests):
                temp_t = 1 + rd.randint(0,n_terrains-2)
                temp_c = checkConflicts(r,c,map,temp_t,terrain_types)

                if temp_c < leastConflicts:
                    best_type = temp_t
                    leastConflicts = temp_c

            map[r,c] = best_type
            



    return map,success




def terrainGen(map,tectonic_map,terrain_types):



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
    display = pygame.Surface((x_res,y_res))

    clock = pygame.time.Clock()
    clock.tick(60)

    #This uses constraint satisfaction to create a terrain set.
    map_size = [np.size(map,0),np.size(map,1)]


    colour_map = np.zeros([map_size[0],map_size[1],3],dtype=int)

    n_terrains = len(terrain_types)

    success = False


    while success == False:
        
        #call least_conflicts until no conflicts are found.

        #DEBUG
        #if it_conf%1 == 0:
        map_display = pygame.surfarray.make_surface(colour_map)
        display.blit(map_display,(0,0))
        screen.blit(pygame.transform.scale(display, screen.get_size()),(0,0))
        pygame.display.update()

        map,success = leastConflicts(map,tectonic_map,terrain_types)

        for r in range(0,map_size[0]):
            for c in range(0,map_size[1]):
                colour_map[r,c,:] = terrain_types[map[r,c]][1]

    #setup colour map
    #for r in range(0,map_size[0]):
    #    for c in range(0,map_size[1]):
    #        colour_map[r,c,:] = terrain_types[map[r,c]][1]

    return map,colour_map