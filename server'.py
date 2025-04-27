import pygame as pg
from balloon import Balloon
from monkey import Monkey
from button import Button
from world import World
from PIL import Image
import math
from monkey_data import MONKEY_DATA



#Constants
WINDOW_WIDTH = 964
WINDOW_HEIGHT = 640
SIDE_PANEL = 250
FPS = 60
SPAWN_COOLDOWN = 400
BUY_COST = 200
UPGRADE_COST = 100
LEVEL_COMPLETE_REWARD = 250

pg.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT + SIDE_PANEL)
screen = pg.display.set_mode(size)
pg.display.set_caption("Bloons TD Battles")
clock = pg.time.Clock()

#game veriables
last_balloon_spawn = pg.time.get_ticks()
placing_monkeys = False
selected_monkey = None

#load images
#map
MAP = pg.image.load("E:\\YA\\BallonsTD_project\\images\\temple.png").convert_alpha()

#side_panel
side_panel = pg.image.load("E:\\YA\\BallonsTD_project\\images\\side_panel.png").convert_alpha()
#Balloons
balloon_images = {
    "red": pg.image.load("E:\\YA\\BallonsTD_project\\images\\balloons\\red_balloon.png").convert_alpha(),
    "blue": pg.image.load("E:\\YA\\BallonsTD_project\\images\\balloons\\blue_balloon.png").convert_alpha(),
    "green": pg.image.load("E:\\YA\\BallonsTD_project\\images\\balloons\\green_balloon.png").convert_alpha(),
    "yellow": pg.image.load("E:\\YA\\BallonsTD_project\\images\\balloons\\yellow_balloon.png").convert_alpha()
}
#Monkeys
cursor_monkey = pg.image.load("E:\\YA\\BallonsTD_project\\images\\Monkeys\\Dart_Monkey.png").convert_alpha()
#Buttons
buy_monkey_image = pg.image.load("E:\\YA\\BallonsTD_project\\images\\Buttons\\buy_dart_monkey.png").convert_alpha()
upgrade_monkey_image = pg.image.load("E:\\YA\\BallonsTD_project\\images\\Buttons\\upgrade_monkey.png").convert_alpha()
#create groups
balloon_group = pg.sprite.Group()
Monkey_group = pg.sprite.Group()

waypoints = [
    (100, 0),
    (100, 105),
    (406, 105),
    (406, 215),
    (303, 215),
    (300, 337),
    (200, 337),
    (200, 448),
    (100, 448),
    (100, 555),
    (405, 560),
    (405, 615)

]


#create buttons
monkey_button = Button(20, WINDOW_HEIGHT + 10, buy_monkey_image, True)
upgrade_button = Button(100, WINDOW_HEIGHT + 10, upgrade_monkey_image, True)

#load fonts
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)

#function for showing text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def create_monkey(mouse_pos):
    # Get the colors in the map
    with open("E:\\YA\\BallonsTD_project\\images\\temple_colors.png", 'rb') as pic:
        img = Image.open(pic)
        width, height = img.size
        pixels = img.load()
        if pixels[mouse_pos] != (0, 0, 0):
            #check that there is no monkey at this spot
            space_is_free = True
            for monkey in Monkey_group:
                if abs(mouse_pos[0] - monkey.rect.center[0]) <= monkey.image.get_size()[0] and abs(mouse_pos[1] - monkey.rect.center[1]) <= monkey.image.get_size()[1]:
                    space_is_free = False
            if space_is_free == True:
                new_monkey = Monkey(mouse_pos)
                Monkey_group.add(new_monkey)
                #deduct cost of monkey
                world.money -= BUY_COST

def select_monkey(nouse_pos):
    for monkey in Monkey_group:
        if abs(mouse_pos[0] - monkey.rect.center[0]) <= monkey.image.get_size()[0] and abs(mouse_pos[1] - monkey.rect.center[1]) <= monkey.image.get_size()[1]:
            return monkey

def clear_selection():
    for monkey in Monkey_group:
        monkey.selected = False


#create world
world = World()
world.process_balloons()

finish = False
while not finish:
    clock.tick(FPS)

    #######################
    # UPDATING SECTION
    #######################


    #update_groups
    balloon_group.update(world)
    Monkey_group.update(balloon_group)


    #hightlight selected monkey
    if selected_monkey:
        selected_monkey.selected = True

    #######################
    # DRAWING SECTION
    #######################
    world.draw(screen, MAP)

    #draw groups
    balloon_group.draw(screen)
    for monkey in Monkey_group:
        monkey.draw(screen)

    draw_text(str(world.health), text_font, "grey100", 0, 0)
    draw_text(str(world.money), text_font, "grey100", 0, 30)
    draw_text(str(world.level), text_font, "grey100", 0, 60)
    #spawn ballons
    if pg.time.get_ticks() - last_balloon_spawn > SPAWN_COOLDOWN:
        if world.spawned_balloons < len(world.balloon_list):
            balloon_type = world.balloon_list[world.spawned_balloons]
            balloon = Balloon(balloon_type, waypoints, balloon_images)
            balloon_group.add(balloon)
            world.spawned_balloons += 1
            last_balloon_spawn = pg.time.get_ticks()

    #check if the wave is finished
    if world.check_level_complete():
        world.money += LEVEL_COMPLETE_REWARD
        world.level += 1
        last_balloon_spawn = pg.time.get_ticks()
        world.reset_level()
        world.process_balloons()

    screen.blit(side_panel, (0, 641))
    #draw buttons
    #button for placing monkeys
    if monkey_button.draw(screen):
        placing_monkeys = True
    if placing_monkeys == True:
        cursor_rect = cursor_monkey.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[1] < WINDOW_HEIGHT:
            screen.blit(cursor_monkey, cursor_rect)
    #if a monkey is selected show upgrade button
    if selected_monkey:
        #if a monkey can be upgraded show upgrade button
        if selected_monkey.upgrade_level < len(MONKEY_DATA):
            if upgrade_button.draw(screen):
                if world.money >= UPGRADE_COST:
                    selected_monkey.upgrade()
                    world.money -= UPGRADE_COST

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finish = True
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Add monkey if mouse is in game area
            if mouse_pos[0] < WINDOW_WIDTH and mouse_pos[1] < WINDOW_HEIGHT:
                selected_monkey = None
                clear_selection()
                if placing_monkeys == True:
                    if world.money >= BUY_COST:
                        create_monkey(mouse_pos)
                else:
                    selected_monkey = select_monkey(mouse_pos)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and placing_monkeys:
            placing_monkeys = False


    pg.display.flip()

pg.quit()


