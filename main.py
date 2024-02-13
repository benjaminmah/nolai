import pygame
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load and play the MP3 file
pygame.mixer.music.load('allergy.mp3')
pygame.mixer.music.set_volume(1.0)  # Ensure the volume is set to be audible
pygame.mixer.music.play()

start_time = time.time()  # Capture start time after music starts

# Load beat times from the simplified beat times file
with open('beat_times.txt', 'r') as f:
    note_timings = [float(line.strip()) for line in f.readlines()]

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RECTANGLE_COLOR = (73, 13, 125)  # Default color for rectangles
HIGHLIGHT_COLOR = (181, 142, 216)  # Color when key is pressed
RECTANGLE_WIDTH = 80
RECTANGLE_HEIGHT = 40
RECTANGLE_GAP = 20
RECTANGLE_Y = SCREEN_HEIGHT - RECTANGLE_HEIGHT - 50

# Define the rhythm pattern
rhythm_pattern = ['f', 'g', 'h', 'j']

# Calculate the starting x-coordinate to center the rectangles
start_x = (SCREEN_WIDTH - (len(rhythm_pattern) * RECTANGLE_WIDTH + (len(rhythm_pattern) - 1) * RECTANGLE_GAP)) // 2

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Load the background image
background_image = pygame.image.load('gidle.jpg').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Notes list
notes = []

def draw_rounded_rect_with_shadow(surface, color, rect, radius):
    # Shadow settings
    shadow_color = (0, 0, 0, 100)  # Semi-transparent black
    shadow_offset_x = 5
    shadow_offset_y = 5
    shadow_rect = pygame.Rect(rect.x + shadow_offset_x, rect.y + shadow_offset_y, rect.width, rect.height)
    
    # Draw shadow
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=radius)
    
    # Draw the rectangle itself
    pygame.draw.rect(surface, color, rect, border_radius=radius)


class Note:
    def __init__(self, x, timing):
        self.x = x
        self.timing = timing  # Note timing from the file
        self.rect = pygame.Rect(self.x, -RECTANGLE_HEIGHT, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
        self.color = RECTANGLE_COLOR
        self.visible = False
        self.exploded = False
        self.done = False
        
        # Calculate the time it takes for the note to reach the button level
        distance_to_button = RECTANGLE_Y + RECTANGLE_HEIGHT
        time_to_reach_button = distance_to_button / SPEED
        
        # Adjust the note's timing so it appears at the button at the specified timing
        self.adjusted_timing = timing - time_to_reach_button
        
        # Calculate the speed dynamically based on the distance and time to reach the button
        self.speed = distance_to_button / time_to_reach_button

    def update(self, current_time):
        # Make note visible based on its timing
        if current_time >= self.adjusted_timing:
            self.visible = True

        if self.visible and not self.exploded:
            progress = (current_time - self.adjusted_timing) * self.speed  # Progress in pixels
            # Update Y-position based on progress, ensuring it stays within valid range
            self.rect.y = min(SCREEN_HEIGHT, -RECTANGLE_HEIGHT + progress)

    def draw(self, surface):
        if self.visible and not self.exploded:  # Draw only if not exploded
            draw_rounded_rect_with_shadow(surface, self.color, self.rect, 10)

    def explode(self):
        self.exploded = True
        self.visible = False  # Hide the note when exploded


# Define the speed at which notes fall (in pixels per second)
SPEED = 500  # Adjust this value as needed

# Adjust the generate_notes function to use the calculated timing
def generate_notes():
    notes.clear()
    for timing in note_timings:
        shuffled_x = random.randrange(0, len(rhythm_pattern))
        x = start_x + shuffled_x * (RECTANGLE_WIDTH + RECTANGLE_GAP)
        notes.append(Note(x, timing))

generate_notes()



# Adjust the draw_rectangles function to call explode method properly
def draw_rectangles():
    for i, key in enumerate(rhythm_pattern):
        is_pressed = pygame.key.get_pressed()[getattr(pygame, 'K_' + key)]
        rect_x = start_x + i * (RECTANGLE_WIDTH + RECTANGLE_GAP)
        rect_color = HIGHLIGHT_COLOR if is_pressed else RECTANGLE_COLOR
        rect_y = RECTANGLE_Y
        rect = pygame.Rect(rect_x, rect_y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
        draw_rounded_rect_with_shadow(screen, rect_color, rect, 10)
        if is_pressed:
            for note in notes:
                if note.rect.colliderect(rect) and note.visible and not note.exploded:
                    note.explode()  # Now properly calls explode method

# Create a semi-transparent black surface
black_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
black_overlay.fill((0, 0, 0, 128))  # Adjust the alpha value as necessary for desired transparency

# Initialize streak counter
streak_counter = 0
longest_streak = 0

# Game loop
running = True
while running:
    current_time = time.time() - start_time  # Current song playback time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen with the background image and the semi-transparent overlay
    screen.blit(background_image, (0, 0))
    screen.blit(black_overlay, (0, 0))
    
    # Draw interaction rectangles
    draw_rectangles()

    # Update and draw notes based on current playback time
    for note in notes:
        note.update(current_time)
        note.draw(screen)

        # Check if note exploded
        if note.exploded and not note.done:
            streak_counter += 1
            longest_streak = max(streak_counter, longest_streak)
            note.done = True
            
        elif note.visible and not note.exploded and current_time > note.timing + 0.25 and not note.done:
            streak_counter = 0
            note.done = True

    # Render and display streak counter in the top right corner
    font = pygame.font.Font(None, 36)  # Choose your font and size
    streak_text = font.render(f"Streak: {streak_counter}", True, (255, 255, 255))  # White color
    screen.blit(streak_text, (SCREEN_WIDTH - streak_text.get_width() - 10, 10))  # Adjust position as needed
            
    # Flip the display buffers to render the current frame
    pygame.display.flip()
    clock.tick(60)  # Maintain a consistent framerate

