import pygame
import time
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RECTANGLE_COLOR = (245, 8, 175, 1)
HIGHLIGHT_COLOR = (245, 175, 224, 1)
BAR_COLOR = (245, 8, 175, 1)
RECTANGLE_WIDTH = 80
RECTANGLE_HEIGHT = 40
RECTANGLE_GAP = 20
RECTANGLE_Y = SCREEN_HEIGHT - RECTANGLE_HEIGHT - 50
PRESSED_OFFSET = 5  # Offset to simulate the button being pressed
SPEED = 500  # Adjust this value as needed

# SONG
songs = {"allergy": ["assets/allergy.mp3", "assets/gidle.jpg", "assets/allergy.txt", {'A': 50000, 'B': 35000, 'C': 20000, 'D': 10000, 'F': 0}],
         "ima": ["assets/ima.mp3", "assets/ima.jpg", "assets/ima.txt", {'A': 120000, 'B': 90000, 'C': 50000, 'D': 10000, 'F': 0}],
         "afterlike": ["assets/afterlike.mp3", "assets/afterlike.jpg", "assets/afterlike.txt", {'A': 120000, 'B': 90000, 'C': 50000, 'D': 10000, 'F': 0}]
         }

song = "allergy"

track = songs[song][0]
image = songs[song][1]
song_notes = songs[song][2]
grade_threshold = songs[song][3]

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rhythm Game")
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.notes = []
        self.score = 0
        self.streak_counter = 0
        self.longest_streak = 0
        self.hit_status = ""
        self.hit_status_time = None  # Time when the last hit status was updated
        self.perfect_hits = 0
        self.good_hits = 0
        self.okay_hits = 0
        self.misses = 0
        self.game_over = False
        self.grade_thresholds = grade_threshold

        self.load_assets()
        self.generate_notes()
        self.main_loop()


    def load_assets(self):
        self.background_image = pygame.image.load(image).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        with open(song_notes, 'r') as f:
            self.note_timings = [float(line.strip()) for line in f.readlines()]

    def generate_notes(self):
        start_x = (SCREEN_WIDTH - (4 * RECTANGLE_WIDTH + (4 - 1) * RECTANGLE_GAP)) // 2
        for timing in self.note_timings:
            x = start_x + random.randrange(0, 4) * (RECTANGLE_WIDTH + RECTANGLE_GAP)
            self.notes.append(Note(x, timing))

    def draw_rectangles(self):
        rhythm_pattern = ['f', 'g', 'h', 'j']
        start_x = (SCREEN_WIDTH - (len(rhythm_pattern) * RECTANGLE_WIDTH + (len(rhythm_pattern) - 1) * RECTANGLE_GAP)) // 2
        for i, key in enumerate(rhythm_pattern):
            is_pressed = pygame.key.get_pressed()[getattr(pygame, 'K_' + key)]
            rect_x = start_x + i * (RECTANGLE_WIDTH + RECTANGLE_GAP)
            rect_color = HIGHLIGHT_COLOR if is_pressed else RECTANGLE_COLOR
            rect_y = RECTANGLE_Y + (PRESSED_OFFSET if is_pressed else 0)
            rect = pygame.Rect(rect_x, rect_y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
            draw_rounded_rect_with_shadow(self.screen, rect_color, rect, 10, not is_pressed)
            if is_pressed:
                self.check_note_collision(rect)

    def check_note_collision(self, rect):
        for note in self.notes:
            if note.rect.colliderect(rect) and note.visible and not note.exploded:
                overlap_area = calculate_overlap_area(note.rect, rect)
                if overlap_area > 0:
                    note.explode()
                    self.update_score_and_streak(overlap_area)

    def update_score_and_streak(self, overlap_area):
        if overlap_area > 800:
            self.hit_status = "Perfect!"
            self.score += min(100 + (self.streak_counter * 10) // 2, 350)
            self.perfect_hits += 1
        elif overlap_area > 200:
            self.hit_status = "Good!"
            self.score += min(50 + (self.streak_counter * 10) // 2, 300)
            self.good_hits += 1
        else:
            self.hit_status = "Okay!"
            self.score += min(10 + (self.streak_counter * 10) // 2, 300)
            self.okay_hits += 1

        self.streak_counter += 1
        self.longest_streak = max(self.streak_counter, self.longest_streak)
        self.hit_status_time = pygame.time.get_ticks()  # Update the time for the hit status

    def reset_streak_on_miss(self, note):
        if note.visible and not note.exploded and time.time() - self.start_time > note.timing + 0.25 and not note.done:
            self.hit_status = "Miss!"
            self.misses += 1
            self.streak_counter = 0
            note.done = True
            self.hit_status_time = pygame.time.get_ticks()

    def display_texts(self):
        custom_font_path = 'commando.ttf'  # Update this path to your font's actual path
        
        # Create a Font object with the custom font file and desired size
        font = pygame.font.Font(custom_font_path, 36)
        
        # The rest of the method remains unchanged
        streak_text = font.render(f"Streak: {self.streak_counter}", True, (255, 255, 255))
        self.screen.blit(streak_text, (SCREEN_WIDTH - streak_text.get_width() - 10, 10))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Display and fade the hit status text
        fade_duration = 600  # Fade duration
        if self.hit_status_time and pygame.time.get_ticks() - self.hit_status_time < fade_duration:
            opacity = max(255 - ((pygame.time.get_ticks() - self.hit_status_time) * 255) / fade_duration, 0)
            hit_text = font.render(self.hit_status, True, (255, 255, 255))
            hit_text_surface = pygame.Surface(hit_text.get_size(), pygame.SRCALPHA)
            hit_text_surface.blit(hit_text, (0, 0))
            hit_text_surface.set_alpha(opacity)
            text_rect = hit_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
            self.screen.blit(hit_text_surface, text_rect)

    def draw_stat_box(self, stats):
        custom_font_path = 'commando.ttf'  # Update this path to your font's actual path
        box_x, box_y, box_width, box_height = 100, 150, 300, 200  # Adjust as needed
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)  # Draw the stats box

        font = pygame.font.Font(custom_font_path, 24)
        line_height = 30
        for i, (label, value) in enumerate(stats.items()):
            # Stat name (left-justified)
            label_surface = font.render(f"{label}:", True, (255, 255, 255))
            self.screen.blit(label_surface, (box_x + 10, box_y + 10 + i * line_height))
            
            # Stat value (right-justified)
            value_surface = font.render(f"{value}", True, (255, 255, 255))
            self.screen.blit(value_surface, (box_x + box_width - value_surface.get_width() - 10, box_y + 10 + i * line_height))

    def calculate_grade(self):
        # Sort the grades based on their thresholds, from highest to lowest
        sorted_grades = sorted(self.grade_thresholds.items(), key=lambda x: x[1], reverse=True)
        return_grade = "F"  # Default grade
        
        for grade, threshold in sorted_grades:
            if self.score >= threshold:
                return_grade = grade
                break  # Stop checking once the correct grade is found
        
        return return_grade

    

    def draw_gradient_grade(self, grade, x, y):
        custom_font_path = 'commando.ttf'  # Update this path to your font's actual path
        
        font = pygame.font.Font(custom_font_path, 300)  # Large font size for the grade
        grade_surface = font.render(grade, True, (181, 142, 216))  # Use the light purple color for simplicity
        self.screen.blit(grade_surface, (x, y))

    
    def display_results_screen(self):
        custom_font_path = 'commando.ttf'  # Update this path to your font's actual path
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Display letter grade with gradient (conceptual, not direct code)
        grade = self.calculate_grade()  # Assume this method calculates and returns the grade based on score
        self.draw_gradient_grade(grade, SCREEN_WIDTH - 300, 150)  # Position for the grade, adjust as needed

        # Prepare stats for the left box
        stats = {
            "Score": self.score,
            "Max Streak": self.longest_streak,
            "Perfects": self.perfect_hits,
            "Goods": self.good_hits,
            "Okays": self.okay_hits,
            "Misses": self.misses
        }
        self.draw_stat_box(stats)

        # Restart prompt
        font = pygame.font.Font(custom_font_path, 36)
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, (50, SCREEN_HEIGHT - 50))


    def restart_game(self):
        # Reset all metrics and start the music again
        self.notes.clear()
        self.score = 0
        self.streak_counter = 0
        self.longest_streak = 0
        self.perfect_hits = 0
        self.good_hits = 0
        self.okay_hits = 0
        self.misses = 0
        # Reset the start time to now
        self.start_time = time.time()
        
        self.load_assets()
        self.generate_notes()
        pygame.mixer.music.play()
        self.game_over = False  # Ensure the game_over flag is also reset
        pygame.mixer.music.play()
    
    def draw_progress_bar(self):
        custom_font_path = 'commando.ttf'
        font = pygame.font.Font(custom_font_path, 24)

        # Constants for appearance
        max_score = max(self.grade_thresholds.values())
        progress_bar_length = SCREEN_WIDTH - 500
        progress_bar_height = 20
        progress_bar_x = (SCREEN_WIDTH - progress_bar_length) // 2
        progress_bar_y = 40
        background_color = (0, 0, 0, 178)  # Adjusted for pygame's lack of direct RGBA support in draw.rect
        fill_color = BAR_COLOR  # Light purple
        marker_color = (255, 255, 255)  # White for grade markers

        # Draw the background of the progress bar (pill-shaped)
        pygame.draw.rect(self.screen, background_color, (progress_bar_x, progress_bar_y, progress_bar_length, progress_bar_height), border_radius=int(progress_bar_height / 2))

        # Ensure there's a minimum filled length to maintain the shape
        min_fill_length = 10  # Minimum visible length of the filled part to ensure pill shape is visible
        score_fill_length = min(self.score / max_score, 1) * progress_bar_length
        fill_length = max(min_fill_length, score_fill_length)

        # Draw the filled part of the progress bar
        pygame.draw.rect(self.screen, fill_color, (progress_bar_x, progress_bar_y, fill_length, progress_bar_height), border_radius=int(progress_bar_height / 2))

        # Draw markers for each grade on top of the bar
        for grade, threshold in self.grade_thresholds.items():
            marker_position = (threshold / max_score) * progress_bar_length + progress_bar_x
            if grade not in ["A", "F"]:
                pygame.draw.line(self.screen, marker_color, (marker_position, progress_bar_y), (marker_position, progress_bar_y + progress_bar_height), 1)
            
            # Display the grade letter above the marker
            grade_text = font.render(grade, True, marker_color)
            self.screen.blit(grade_text, (marker_position - grade_text.get_width() / 2, progress_bar_y - grade_text.get_height() - 5))




    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart_game()
                        self.game_over = False

            if not pygame.mixer.music.get_busy() and not self.game_over:
                self.game_over = True

            if not self.game_over:
                self.screen.blit(self.background_image, (0, 0))
                black_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                black_overlay.fill((0, 0, 0, 180))
                self.screen.blit(black_overlay, (0, 0))
                self.draw_rectangles()
                for note in self.notes:
                    note.update(time.time() - self.start_time)
                    note.draw(self.screen)
                    self.reset_streak_on_miss(note)
                self.display_texts()
                self.draw_progress_bar()  # Update and render the progress bar
            else:
                self.display_results_screen()

            pygame.display.flip()
            self.clock.tick(60)


class Note:
    def __init__(self, x, timing):
        self.x = x
        self.timing = timing
        self.rect = pygame.Rect(self.x, -RECTANGLE_HEIGHT, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
        self.color = RECTANGLE_COLOR
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

def draw_rounded_rect_with_shadow(surface, color, rect, radius, shadow=True):
    shadow_color = (0, 0, 0, 100)
    shadow_offset_x = 5
    shadow_offset_y = 5
    if shadow:
        shadow_rect = pygame.Rect(rect.x + shadow_offset_x, rect.y + shadow_offset_y, rect.width, rect.height)
        pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=radius)
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def calculate_overlap_area(rect1, rect2):
    x1 = max(rect1.left, rect2.left)
    y1 = max(rect1.top, rect2.top)
    x2 = min(rect1.right, rect2.right)
    y2 = min(rect1.bottom, rect2.bottom)
    overlap_width = x2 - x1
    overlap_height = y2 - y1
    if overlap_width > 0 and overlap_height > 0:
        return overlap_width * overlap_height
    return 0

if __name__ == "__main__":
    Game()
