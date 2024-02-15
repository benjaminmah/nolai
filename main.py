import pygame
from settings import *
from game import Game, song_select_screen

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.music.set_volume(0.7)
    pygame.display.set_caption("Nolai: A Rhythm Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Default font for simplicity

    selected_song = song_select_screen(screen, font)
    game = Game(selected_song, screen, font)
