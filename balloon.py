import pygame as pg
from pygame.math import Vector2
from balloon_data import BALLOON_DATA

KILL_REWARD = 5

balloon_images = {
        "red": pg.image.load("images\\balloons\\red_balloon.png"),
        "blue": pg.image.load("images\\balloons\\blue_balloon.png"),
        "green": pg.image.load("images\\balloons\\green_balloon.png"),
        "yellow": pg.image.load("images\\balloons\\yellow_balloon.png")
    }
class Balloon(pg.sprite.Sprite):
    def __init__(self,balloon_type,  waypoints):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = BALLOON_DATA.get(balloon_type)["health"]
        self.speed = BALLOON_DATA.get(balloon_type)["speed"]
        self.type = balloon_type
        self.rect = pg.Rect(0, 0, 40, 52)
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.check_alive(world)
    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos

            # calculate distance to target
            dist = self.movement.length()
            # check if remaining distance is greater than speed
            if dist >= self.speed:
                self.pos += self.movement.normalize() * self.speed
            else:
                if dist != 0:
                    self.pos = self.waypoints[self.target_waypoint]
                self.target_waypoint += 1
            self.rect.center = self.pos
        else:
            #balloon has reached the end of the path
            self.kill()
            world.health -= self.health
            world.missed_balloons += 1

    def reduce_balloon_level(self):
        types = ["red", "blue", "green", "yellow"]
        self.speed = BALLOON_DATA[types[self.health - 1]]["speed"]
        self.type = types[self.health - 1]
    def check_alive(self, world):
        if self.health <= 0:
            world.killed_balloons += 1
            world.money += 5
            self.kill()

    def draw(self, surface):
        global balloon_images
        surface.blit(balloon_images[self.type].convert_alpha(), self.rect)

