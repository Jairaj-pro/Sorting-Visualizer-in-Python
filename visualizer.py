import pygame
import math
import random
pygame.init()

class draw_information:
    BLACK = 0,0,0
    COMPLETED = False
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED=255,0,0
    BACKGROUND_COLOR=WHITE
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    SMALL_FONT = pygame.font.SysFont("comicsans",12)
    FONT = pygame.font.SysFont("comicsans",30)
    LARGE_FONT= pygame.font.SysFont("comicsans",40)
    def __init__(self, width, height, lst):
        self.width=width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("SORTING ALGORITHM VISUALIZER")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.max_value = max(lst)
        self.min_value = min(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD //2



def genereate_starting_list(n,max_val,min_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val , max_val)
        lst.append(val)
    return lst



def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    if ascending:
        text="Ascending"
    else:
        text="Descending"
    title=draw_info.LARGE_FONT.render(algo_name+" - "+text,1, draw_info.GREEN)
    draw_info.window.blit(title,(draw_info.width//2 - title.get_width()/2,0))
    controls=draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Desceding", 1, draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width//2 - controls.get_width()/2,45))
    sorting=draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width//2 - sorting.get_width()/2,75))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg = False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect (draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)  
    for i,val in enumerate(lst):
        x= draw_info.start_x + i*draw_info.block_width
        y= draw_info.height-(val-draw_info.min_value)*draw_info.block_height
        color=draw_info.GRADIENTS[i%3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width, draw_info.height))
        text = draw_info.SMALL_FONT.render("%d"%val,1, draw_info.BLACK)
        draw_info.window.blit(text,(x+2,y+2))
    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]
            if(num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN, j+1: draw_info.RED}, True )
                yield True
    draw_info.COMPLETED = True
    return lst



def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i>0 and lst[i-1] > current and ascending
            descending_sort = i>0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i-=1
            lst[i] = current
            draw_list(draw_info,{i-1:draw_info.GREEN,i:draw_info.RED},True) 
            yield True
    draw_info.COMPLETED = True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()
    n=50
    min_val = 0
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None
    max_val = 100
    sorting=False
    ascending=True
    lst = genereate_starting_list(n,max_val,min_val)
    draw_info = draw_information(1000,600,lst)
    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name,ascending )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = genereate_starting_list(n,max_val,min_val)
                draw_info.set_list(lst)
                sorting=False
            elif (event.key == pygame.K_SPACE and sorting == False):
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
               
            elif (event.key == pygame.K_a and not sorting):
                ascending = True
            elif (event.key == pygame.K_d and not sorting):
                ascending = False
            elif (event.key == pygame.K_i and not sorting):
                sorting_algorithm=insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif (event.key == pygame.K_b and not sorting):
                sorting_algorithm=bubble_sort
                sorting_algorithm_name = "Bubble Sort"
        # title=draw_info.LARGE_FONT.render("Done",1, draw_info.BLACK)
        # draw_info.window.blit(title,(draw_info.width//2 - title.get_width()/2,0))
        # pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()