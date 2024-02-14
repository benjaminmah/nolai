import pygame
from settings import *
from utils import draw_rounded_rect_with_shadow

class Note:
    def __init__(self, x, timing):
        self.x = x
        self.timing = timing
        self.rect = pygame.Rect(self.x, -RECTANGLE_HEIGHT, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
        self.color = NOTE_COLOR
        self.visible = False
        self.exploded = False
        self.done = False
        self.adjust_timing()

    def adjust_timing(self):
        distance_to_button = RECTANGLE_Y + RECTANGLE_HEIGHT
        self.adjusted_timing = self.timing - distance_to_button / SPEED
        self.speed = distance_to_button / (distance_to_button / SPEED)

    def update(self, current_time):
        if current_time >= self.adjusted_timing:
            self.visible = True
        if self.visible and not self.exploded:
            self.rect.y = min(SCREEN_HEIGHT, -RECTANGLE_HEIGHT + (current_time - self.adjusted_timing) * self.speed)

    def draw(self, surface):
        if self.visible and not self.exploded:
            draw_rounded_rect_with_shadow(surface, self.color, self.rect, 10)

    def explode(self):
        self.exploded = True
        self.visible = False