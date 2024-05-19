import pygame
import numpy as np
import time
import random

def generate_random_number(limit):
    return random.randint(0, limit)

color_bg = (10,10,10)
color_grid = (40,40,40)
color_die_next = (170,170,170)
color_alive_next = (255,255,255)

def update(screen,cells,size,with_progress=False):
    updated_cells = np.zeros((cells.shape[0],cells.shape[1]))
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row,col]
        color = color_bg if cells[row,col] == 0 else color_alive_next

        #GAME RULES
        if cells[row,col] == 1:
            if alive < 2 or alive>3:
                if with_progress:
                    color = color_die_next
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next
        else:
            if alive ==3:
                updated_cells[row, col] = 1

                if with_progress:
                    color = color_alive_next
        pygame.draw.rect(screen,color,(col*size,row*size,size-1,size-1))
    return(updated_cells)

def coordinates_to_lists(coordinates):
    x_coordinates = []
    y_coordinates = []
    for i, value in enumerate(coordinates):
        if value == 1:
            x_coordinates.append(i % 4)
            y_coordinates.append(i // 4)
    return x_coordinates, y_coordinates

def main(coordinates):
    start_timer = time.time()
    x_coords, y_coords = coordinates_to_lists(coordinates)

    pygame.init()
    screen = pygame.display.set_mode((800,600))    
    cells = np.zeros((60,80))

    #random_cells = 0 
    cole = []
    rowe = []
    for i in range(len(x_coords)):
        cole.append(x_coords[i]+25)
        rowe.append(y_coords[i]+33)
        #generate_random_number(60 or 80)

    for i in range(len(cole)):
        cells[cole[i],rowe[i]] = 1

    screen.fill(color_grid)
    update(screen,cells,10)
    pygame.display.flip()
    pygame.display.update()


    running = False
    most_cells = np.sum(cells)
    while True:
        if pygame.time.get_ticks()/1000 > 5000:
            pygame.quit()
            try:
                end_timer = time.time()
                total_time = end_timer - start_timer
                print(f"Current score: {np.sum(cells)}, Time to stabilise: {total_time:.4f} seconds")
                print(f"Score: {most_cells}")
                return(most_cells)
            except:
                return(0)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    end_timer = time.time()
                    total_time = end_timer - start_timer
                    print(f"Current score: {np.sum(cells)}, Time to stabilise: {total_time:.4f} seconds")
                    print(f"Best score: {most_cells}")
                    return(most_cells)
                except:
                    return(0)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen,cells,10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                print("cells:",pos[1] // 10, pos[0] // 10)
                cells[pos[1] // 10, pos[0] // 10 ] = 1
                update(screen,cells,10)
                pygame.display.update()
        screen.fill(color_grid)

        if running:
            cells = update(screen,cells,10, with_progress=True)
            pygame.display.update()

        if most_cells < np.sum(cells):
            most_cells = np.sum(cells)
            #print(f"New Max! Amount of cells:{most_cells}")
        time.sleep(0.001)


if __name__ == '__main__':
    #main([1, 0, 1, 1, 0, 1, 1, 1, 1])#3x3 nice symmetrical pattern, score: 201 stabilise: 55 time:8
    #main([0, 0, 1, 1, 0, 1, 1, 1, 1])#3x3 random and spreading pattern score: 278 stabilise: 95 time:33
    #main([1, 0, 1, 0, 1, 1, 0, 0, 1])#3x3 probably the coolest random score: 267 stabilise 95 time:16
    #main([0, 0, 1, 0, 1, 0, 1, 1, 1]) #3x3 random and spreading pattern, score: 317 stabilise: 136 time:28s
    main([1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1])
    #main([1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0]) #4x4 Nice curly pattern, score: 169 stabilise: 49 time:11s
    #main([0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1]) #4x4 Firework score: 239 sta: 72 time:19
    pass