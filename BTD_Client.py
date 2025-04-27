import pygame as pg
from balloon import Balloon
from monkey import Monkey
from button import Button
from world import World
from PIL import Image
from sys import exit
from monkey_data import MONKEY_DATA
import socket
from tcp_by_size import *
import pickle

WINDOW_WIDTH = 964
WINDOW_HEIGHT = 640
SIDE_PANEL = 170
FPS = 70
SPAWN_COOLDOWN = 400
BUY_COST = 200
LEVEL_COMPLETE_REWARD = 250

player_num = 0 #global
finish = False
game_crashed = False
game_won = False
send_player_num = 'PLRN' #player number
send_balloons = 'SBLN'
send_monkeys = 'SMKS'
send_health = 'SOHP'
exit_msg = 'EXIT'

def start_screen(sock, screen, clock):
    global finish, game_crashed
    ready = False
    ready_image = pg.image.load("images\\ready_button.png").convert_alpha()
    waiting_image = pg.image.load("images\\waiting_for_player.png").convert_alpha()
    ready_button = Button(400, 400, ready_image, True)
    start_screen_pic = pg.image.load("images\\start_image.png").convert_alpha()
    screen.blit(start_screen_pic, (0, 0))
    screen.blit(ready_image, (400, 400))
    pg.display.flip()
    while not ready:
        clock.tick(5)

        for event in pg.event.get():
            # mouse click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if ready_button.rect.collidepoint(mouse_pos) and ready_button.clicked == False:
                    send_with_size(sock, "READY")
                    ready_button.clicked = True
                    screen.blit(start_screen_pic, (0, 0))
                    screen.blit(waiting_image, (300, 400))
                    pg.display.flip()
                    try:
                        data = recv_by_size(sock)
                        if data == "START":
                            ready = True

                    except:
                        print("error")
            elif event.type == pg.QUIT:
                send_with_size(sock, exit_msg)
                game_crashed = True
                ready = True
                finish = True
                break





def main(ip):
    global player_num, finish, game_won, game_crashed
    connected = False
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    try:
        client_sock.connect((ip, port))
        print(f"Connect succeeded {ip}:{port}")
        connected = True
    except:
        print(f"Error while trying to connect")


    #set py game screen
    pg.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT + SIDE_PANEL)
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Bloons TD Battles")
    clock = pg.time.Clock()


    #call start screen function
    start_screen(client_sock, screen, clock)

    client_sock.settimeout(5)
    # get player num
    try:
        msg = recv_by_size(client_sock)
        msg = msg.split('~')
        if msg[0] == send_player_num:
            player_num = int(msg[1])
    except:
        send_with_size(client_sock, exit_msg)
        pg.quit()
        client_sock.close()
        exit()


    player_width = (0,0)
    if player_num == 1:
        player_width = (0, WINDOW_WIDTH / 2 - 27)
    elif player_num == 2:
        player_width = (WINDOW_WIDTH / 2 + 27, WINDOW_WIDTH)
    else:
        print("error with player num")





    # game veriables
    last_balloon_spawn = pg.time.get_ticks()
    placing_monkeys = False
    selected_monkey = None
    upgrade_cost = 100
    # load images
    # map
    MAP = pg.image.load("images\\temple.png").convert_alpha()

    # side_panel
    side_panel = pg.image.load("images\\side_panel.png").convert_alpha()
    # Balloons

    # Monkeys
    cursor_monkey = pg.image.load("images\\Monkeys\\Dart_Monkey.png").convert_alpha()
    # Buttons
    buy_monkey_image = pg.image.load("images\\Buttons\\buy_dart_monkey.png").convert_alpha()
    upgrade_monkey_image = pg.image.load("images\\Buttons\\upgrade_monkey.png").convert_alpha()
    # create groups
    balloon_group = pg.sprite.Group()
    Monkey_group = pg.sprite.Group()

    #other players group
    balloon_group2 = pg.sprite.Group()
    Monkey_group2 = pg.sprite.Group()
    other_health = 50

    if player_num == 1:
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
    else:
        waypoints = [
        (WINDOW_WIDTH - 100, 0),
        (WINDOW_WIDTH - 100, 105),
        (WINDOW_WIDTH - 406, 105),
        (WINDOW_WIDTH - 406, 215),
        (WINDOW_WIDTH - 303, 215),
        (WINDOW_WIDTH - 300, 337),
        (WINDOW_WIDTH - 200, 337),
        (WINDOW_WIDTH - 200, 448),
        (WINDOW_WIDTH - 100, 448),
        (WINDOW_WIDTH - 100, 555),
        (WINDOW_WIDTH - 405, 560),
        (WINDOW_WIDTH - 405, 615)
        ]

    # create buttons
    monkey_button = Button(20, WINDOW_HEIGHT + 10, buy_monkey_image, True)
    upgrade_button = Button(100, WINDOW_HEIGHT + 10, upgrade_monkey_image, True)

    # load fonts
    text_font = pg.font.SysFont("Consolas", 24, bold=True)
    large_font = pg.font.SysFont("Consolas", 36)


    # function for showing text on screen
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def create_monkey(mouse_pos):
        # Get the colors in the map
        with open("images\\temple_colors.png", 'rb') as pic:
            img = Image.open(pic)
            width, height = img.size
            pixels = img.load()
            if pixels[mouse_pos] != (0, 0, 0):
                # check that there is no monkey at this spot
                space_is_free = True
                for monkey in Monkey_group:
                    if abs(mouse_pos[0] - monkey.rect.center[0]) <= 57 and abs(
                            mouse_pos[1] - monkey.rect.center[1]) <= 56:
                        space_is_free = False
                if space_is_free == True:
                    new_monkey = Monkey(mouse_pos)
                    Monkey_group.add(new_monkey)
                    # deduct cost of monkey
                    world.money -= BUY_COST

    def select_monkey(nouse_pos):
        for monkey in Monkey_group:
            if abs(mouse_pos[0] - monkey.rect.center[0]) <= 57 and abs(
                    mouse_pos[1] - monkey.rect.center[1]) <= 56:
                return monkey

    def clear_selection():
        for monkey in Monkey_group:
            monkey.selected = False

    # create world
    world = World()
    world.process_balloons()


    while not finish:
        clock.tick(FPS)

        #######################
        # UPDATING SECTION
        #######################

        if(world.health)<= 0:
            break
        elif other_health <= 0:
            game_won = True
            break


        # update_groups
        balloon_group.update(world)
        Monkey_group.update(balloon_group, player_width)

        #send balloon group
        to_send = send_balloons.encode() + '~'.encode() + pickle.dumps(balloon_group)
        send_with_size(client_sock, to_send)
        #recv other player balloons
        try:
            data = recv_by_size(client_sock, 'bytes')
            if data[:4].decode() == send_balloons:
                balloon_group2 = pickle.loads(data[5:])
            elif data[:4].decode() == exit_msg:
                game_won = True
                break
        except:
            send_with_size(client_sock, exit_msg)
            game_crashed = True
            break

        # send monkeys group
        to_send = send_monkeys.encode() + '~'.encode() + pickle.dumps(Monkey_group)
        send_with_size(client_sock, to_send)
        #recv other player monkeys
        try:
            data = recv_by_size(client_sock, 'bytes')
            if data[:4].decode() == send_monkeys:
                Monkey_group2 = pickle.loads(data[5:])
            elif data[:4].decode() == exit_msg:
                game_won = True
                break
        except:
            send_with_size(client_sock, exit_msg)
            game_crashed = True
            break


        #send health
        to_send = send_health + '~' + str(world.health)
        send_with_size(client_sock, to_send)
        #recv other player's health
        try:
            data = recv_by_size(client_sock)
            data = data.split('~')
            if data[0] == send_health:
                other_health = int(data[1])
            elif data[0].decode() == exit_msg:
                game_won = True
                break
        except:
            send_with_size(client_sock, exit_msg)
            game_crashed = True
            break

        # hightlight selected monkey
        if selected_monkey:
            selected_monkey.selected = True

        #######################
        # DRAWING SECTION
        #######################
        world.draw(screen, MAP)
        screen.blit(side_panel, (0, WINDOW_HEIGHT))
        # draw groups
        for balloon in balloon_group:
            balloon.draw(screen)
        for monkey in Monkey_group:
            monkey.draw(screen)

        for balloon in balloon_group2:
            balloon.draw(screen)
        for monkey in Monkey_group2:
            monkey.draw(screen)


        if player_num == 1:
            # player on left side so show health on left side
            draw_text(str(world.health), text_font, "green", 0, 0)
            draw_text(str(other_health), text_font, "grey100", WINDOW_WIDTH - 50, 0)
        else:
            # player on right side so show health on right side
            draw_text(str(world.health), text_font, "green", WINDOW_WIDTH - 50, 0)
            draw_text(str(other_health), text_font, "grey100", 0, 0)
        draw_text(str(world.money) + "$", text_font, "grey100", 465, WINDOW_HEIGHT + SIDE_PANEL - 93)
        draw_text("Round", text_font, "orange", 450, 30)
        draw_text(str(world.level), text_font, "orange", 475, 60)
        # spawn ballons
        if pg.time.get_ticks() - last_balloon_spawn > SPAWN_COOLDOWN:
            if world.spawned_balloons < len(world.balloon_list):
                balloon_type = world.balloon_list[world.spawned_balloons]
                balloon = Balloon(balloon_type, waypoints)
                balloon_group.add(balloon)
                world.spawned_balloons += 1
                last_balloon_spawn = pg.time.get_ticks()

        # check if the wave is finished
        if world.check_level_complete():
                world.money += LEVEL_COMPLETE_REWARD
                world.level += 1
                last_balloon_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_balloons()


        #draw buttons
        #button for placing monkeys
        draw_text(str(BUY_COST) + "$", text_font, "grey100", 25, WINDOW_HEIGHT + 80)
        if monkey_button.draw(screen):
            placing_monkeys = True
        if placing_monkeys == True:
            cursor_rect = cursor_monkey.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[1] < WINDOW_HEIGHT:
                screen.blit(cursor_monkey, cursor_rect)
        # if a monkey is selected show upgrade button
        if selected_monkey:
            # if a monkey can be upgraded show upgrade button
            if selected_monkey.upgrade_level < len(MONKEY_DATA):
                upgrade_cost = selected_monkey.upgrade_level * 50 + 50
                draw_text(str(upgrade_cost) + "$", text_font, "grey100", 120, WINDOW_HEIGHT + 105)
                if upgrade_button.draw(screen):
                    if world.money >= upgrade_cost:
                        selected_monkey.upgrade()
                        world.money -= upgrade_cost
                        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                send_with_size(client_sock, exit_msg)
                finish = True
                game_crashed = True
                break


            # mouse click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                # Add monkey if mouse is in game area
                if mouse_pos[0] < player_width[1] and mouse_pos[0] > player_width[0] and mouse_pos[1] < WINDOW_HEIGHT:
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

    client_sock.close()
    victory_pic = pg.image.load("images\\victory.png").convert_alpha()
    defeat_pic = pg.image.load("images\\defeat.png").convert_alpha()
    if not game_crashed:
        if game_won:
            screen.blit(victory_pic, (0, 0))
        else:
            screen.blit(defeat_pic, (0, 0))
        pg.display.flip()
        close_ending_screen = False
        while not close_ending_screen:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    close_ending_screen = True
                    break

    pg.quit()
    exit()


if __name__ == '__main__':
    main("10.68.121.228")