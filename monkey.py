import pygame as pg
import math
from monkey_data import MONKEY_DATA

#animation variables
Animation_pic1 = pg.image.load("images\\Monkeys\\Dart_Monkey.png")
Animation_pic2 = pg.image.load("images\\Monkeys\\Dart_Monkey1.png")
animation_list = [Animation_pic1, Animation_pic2, Animation_pic1]

class Monkey(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = MONKEY_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = MONKEY_DATA[self.upgrade_level - 1].get("cooldown")
        self.damage = 1
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None


        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.x = pos[0]
        self.y = pos[1]
        self.angle = 90
        self.rect = pg.Rect(0,0,57,56)
        self.rect.center = (self.x, self.y)




    def update(self, balloon_group, player_width):
        #if target picked, start firing animation
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(balloon_group, player_width)


    def pick_target(self, balloon_group, player_width):
        x_dist = 0
        y_dist = 0

        for balloon in balloon_group:
            if balloon.health > 0:
                x_dist = balloon.pos[0] - self.x
                y_dist = balloon.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range and player_width[1] > balloon.pos[0] > player_width[0]:
                    self.target = balloon
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #damage enemy
                    self.target.health -= self.damage
                    if self.target.health > 0:
                        self.target.reduce_balloon_level()
                    break
    def play_animation(self):
        Animation_delay = 100
        #update image
        original_image = animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > Animation_delay:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if animation is finished
            if self.frame_index >= len(animation_list):
                self.frame_index = 0
                #record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = MONKEY_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = MONKEY_DATA[self.upgrade_level - 1].get("cooldown")

        #upgrade range circle
        range_image = pg.Surface((self.range * 2, self.range * 2))
        range_image.fill((0, 0, 0))
        range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(range_image, "grey100", (self.range, self.range), self.range)
        range_image.set_alpha(100)
        range_rect = range_image.get_rect()
        range_rect.center = self.rect.center



    def draw(self, surface):
        original_image = animation_list[self.frame_index]
        image = pg.transform.rotate(original_image, self.angle - 90)
        self.rect = image.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(image.convert_alpha(), self.rect)
        if self.selected:
            # create circle to show range
            range_image = pg.Surface((self.range * 2, self.range * 2))
            range_image.fill((0, 0, 0))
            range_image.set_colorkey((0, 0, 0))
            pg.draw.circle(range_image, "grey100", (self.range, self.range), self.range)
            range_image.set_alpha(100)
            range_rect = range_image.get_rect()
            range_rect.center = self.rect.center
            surface.blit(range_image, range_rect)

