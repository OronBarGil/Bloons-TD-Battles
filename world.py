import pygame as pg
import random

class World():
    def __init__(self):
        self.level = 1
        self.health = 50
        self.money = 650
        self.waypoints = []
        self.balloon_list = []
        self.spawned_balloons = 0
        self.killed_balloons = 0
        self.missed_balloons = 0
        self.balloons = {
            "red": 20,
            "blue": 0,
            "yellow": 0,
            "green": 0
        }
    def process_balloons(self):
        if self.balloons["red"] >= 2:
            self.balloons["red"] -= (2 * (self.level - 1))
        if self.level % 2 == 0:
            self.balloons["blue"] += self.level
        if self.level % 3 == 0:
            self.balloons["green"] += self.level
        if self.level % 5 == 0:
            self.balloons["yellow"] += self.level
        for balloon_type in self.balloons:
            balloons_to_spawn = self.balloons[balloon_type]
            for balloon in range(balloons_to_spawn):
                self.balloon_list.append(balloon_type)
        #randomize ballons spawns
        random.shuffle(self.balloon_list)

    def check_level_complete(self):
        if self.killed_balloons + self.missed_balloons == len(self.balloon_list):
            return True

    def reset_level(self):
        self.balloon_list = []
        self.spawned_balloons = 0
        self.killed_balloons = 0
        self.missed_balloons = 0
    def draw(self, surface, image):
        surface.blit(image, (0,0))