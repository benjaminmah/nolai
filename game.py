import pygame
import time
import random
from settings import *
from utils import draw_rounded_rect_with_shadow, calculate_overlap_area, wrap_text, preprocess_lyrics
from note import Note

def song_select_screen(screen, font):
    running = True
    song_keys = list(songs.keys())
    selected_index = 0
    while running:
        screen.fill((0, 0, 0))  # Fill screen with black
        for i, key in enumerate(song_keys):
            if i == selected_index:
                text_surf = font.render(f"> {key}", True, HIGHLIGHT_COLOR)  # Highlight selected song
            else:
                text_surf = font.render(key, True, (255, 255, 255))  # Other songs
            screen.blit(text_surf, (100, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(song_keys) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    return song_keys[selected_index]

class Game:
    def __init__(self, song_choice, screen, font):
        self.song_choice = song_choice
        self.track, self.image, self.song_notes, self.grade_threshold, self.lyrics, self.lyric_font = songs[song_choice]
        self.screen = screen
        self.font = font
        font2 = pygame.font.Font(self.lyric_font, 18)  # Use the same font size as in display_lyrics
        self.processed_lyrics = preprocess_lyrics(font2, 160, self.lyrics)
        self.animation_played = False
        self.result_effects = False
        self.letter_sound = pygame.mixer.Sound('assets/letter_sound.mp3')
        self.load_assets()
        self.reset_game()
        self.main_loop()

    def load_assets(self):
        self.background_image = pygame.image.load(self.image).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mixer.music.load(self.track)
        pygame.mixer.music.set_volume(1.0)
        with open(self.song_notes, 'r') as f:
            self.note_timings = [float(line.strip()) for line in f.readlines()]
        self.grade_thresholds = self.grade_threshold

    def reset_game(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rhythm Game")
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.notes = []
        self.score = 0
        self.streak_counter = 0
        self.longest_streak = 0
        self.hit_status = ""
        self.hit_status_time = None
        self.perfect_hits = 0
        self.good_hits = 0
        self.okay_hits = 0
        self.misses = 0
        self.game_over = False
        self.animation_played = False
        self.result_effects = False
        pygame.mixer.music.play(0) 
        self.generate_notes()

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
        if overlap_area > 700:
            self.hit_status = "perfect!"
            self.score += min(100 + (self.streak_counter * 10) // 2, 350)
            self.perfect_hits += 1
        elif overlap_area > 150:
            self.hit_status = "good!"
            self.score += min(50 + (self.streak_counter * 10) // 2, 300)
            self.good_hits += 1
        else:
            self.hit_status = "okay!"
            self.score += min(10 + (self.streak_counter * 10) // 2, 360)
            self.okay_hits += 1

        self.streak_counter += 1
        self.longest_streak = max(self.streak_counter, self.longest_streak)
        self.hit_status_time = pygame.time.get_ticks()  # Update the time for the hit status

    def reset_streak_on_miss(self, note):
        if note.visible and not note.exploded and time.time() - self.start_time > note.timing + 0.25 and not note.done:
            self.hit_status = "miss!"
            self.misses += 1
            self.streak_counter = 0
            note.done = True
            self.hit_status_time = pygame.time.get_ticks()

    def display_texts(self):        
        # Create a Font object with the custom font file and desired size
        font = pygame.font.Font(CUSTOM_FONT, 30)
        
        score_text = font.render(f"{self.score}", True, (255, 255, 255))
        text_width = score_text.get_width()  # Get the width of the rendered text
        self.screen.blit(score_text, (SCREEN_WIDTH - text_width - 20, 20))

        # Display and fade the hit status text
        fade_duration = 600  # Fade duration
        if self.hit_status_time and pygame.time.get_ticks() - self.hit_status_time < fade_duration:
            opacity = max(255 - ((pygame.time.get_ticks() - self.hit_status_time) * 255) / fade_duration, 0)
            font = pygame.font.Font(CUSTOM_FONT, 50)
            if self.hit_status == 'perfect!':
                text_color = (51, 178, 240)
            elif self.hit_status == 'good!':
                text_color = (50, 205, 50)
            elif self.hit_status == 'okay!':
                text_color = (255, 255, 0)
            else:
                text_color = (178, 34, 34)

            hit_text = font.render(self.hit_status, True, text_color)
            hit_text_surface = pygame.Surface(hit_text.get_size(), pygame.SRCALPHA)
            hit_text_surface.blit(hit_text, (0, 0))
            hit_text_surface.set_alpha(opacity)
            text_rect = hit_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            self.screen.blit(hit_text_surface, text_rect)

            font = pygame.font.Font(CUSTOM_FONT, 35)
            streak_text = font.render(str(self.streak_counter), True, (255, 255, 255))
            streak_text_surface = pygame.Surface(streak_text.get_size(), pygame.SRCALPHA)
            streak_text_surface.blit(streak_text, (0, 0))
            streak_text_surface.set_alpha(opacity)
            text_rect2 = streak_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5))
            self.screen.blit(streak_text_surface, text_rect2)

    def draw_stat_box(self, stats):
        box_x, box_y, box_width, box_height = 100, 150, 300, 190  # Adjust as needed
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2, border_radius=10)  # Draw the stats box

        font = pygame.font.Font(CUSTOM_FONT, 24)
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
        return_grade = "f"  # Default grade
        
        for grade, threshold in sorted_grades:
            if self.score >= threshold:
                return_grade = grade
                break  # Stop checking once the correct grade is found
        
        return return_grade

    

    def draw_gradient_grade(self, grade, x, y, result_effects):


        font = pygame.font.Font(CUSTOM_FONT, 300)  # Large font size for the grade
        grade_surface = font.render(grade, True, (181, 142, 216))  # Use the light purple color for simplicity
        self.screen.blit(grade_surface, (x, y))

        if not result_effects:
            pygame.mixer.Sound.play(self.letter_sound)
            pygame.display.flip()
        else:
            pygame.display.flip()

    def animate_stats(self, final_stats):
        initial_stats = {key: 0 for key in final_stats.keys()}  # Initialize all stats at 0
        increment_speed = 2  # Time between updates in milliseconds, adjust for desired speed
        stats_keys = list(final_stats.keys())  # Get a list of the stat keys to manage order
        current_stat_index = 0  # Start with the first stat

        while current_stat_index < len(stats_keys):
            stat_key = stats_keys[current_stat_index]
            if stat_key == "score":
                initial_stats[stat_key] = final_stats[stat_key]
            else:
                while initial_stats[stat_key] < final_stats[stat_key]:
                    initial_stats[stat_key] += 1  # Increment by 1 for other stats

                    self.screen.fill((0, 0, 0))  # Clear the screen for redrawing
                    self.draw_stat_box(initial_stats)  # Draw the box with updated stats

                    # Re-draw any other UI elements here
                    
                    pygame.display.flip()  # Update the display with the new drawings

                    pygame.time.delay(increment_speed)

                    # Process Pygame events to keep the window responsive
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return

            current_stat_index += 1  # Move to the next stat once the current is complete
    
    def draw_stat_box(self, stats):
        box_x, box_y, box_width, box_height = 100, 150, 300, 190  # Adjust as needed
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2, border_radius=10)  # Draw the stats box

        font = pygame.font.Font(CUSTOM_FONT, 24)
        line_height = 30
        for i, (label, value) in enumerate(stats.items()):
            # Stat name (left-justified)
            label_surface = font.render(f"{label}:", True, (255, 255, 255))
            self.screen.blit(label_surface, (box_x + 10, box_y + 10 + i * line_height))
            
            # Stat value (right-justified)
            value_surface = font.render(f"{value}", True, (255, 255, 255))
            self.screen.blit(value_surface, (box_x + box_width - value_surface.get_width() - 10, box_y + 10 + i * line_height))

    def display_results_screen(self):
    
        # Prepare final stats for the left box
        final_stats = {
            "score": self.score,
            "max streak": self.longest_streak,
            "perfects": self.perfect_hits,
            "goods": self.good_hits,
            "okays": self.okay_hits,
            "misses": self.misses
        }
        # Animate stats from 0 to their final values
        if not self.animation_played:
            self.animate_stats(final_stats)
            self.animation_played = True
        else:
            self.draw_stat_box(final_stats)

        # Display letter grade with gradient (conceptual, not direct code)
        grade = self.calculate_grade()  # Assume this method calculates and returns the grade based on score
        if not self.result_effects:
            self.draw_gradient_grade(grade, SCREEN_WIDTH - 300, 150, False)  # Position for the grade, adjust as needed

            pygame.time.delay(1000)
            # Restart prompt
            font = pygame.font.Font(CUSTOM_FONT, 30)
            restart_text = font.render("press r to restart", True, (255, 255, 255))
            menu_text = font.render("press m to return to song select", True, (255, 255, 255))
            self.screen.blit(restart_text, (50, SCREEN_HEIGHT - 50))
            self.screen.blit(menu_text, (50, SCREEN_HEIGHT - 100))

            pygame.display.flip()
            
            self.result_effects = True

        self.draw_gradient_grade(grade, SCREEN_WIDTH - 300, 150, True)  # Position for the grade, adjust as needed

        # Restart prompt
        font = pygame.font.Font(CUSTOM_FONT, 30)
        restart_text = font.render("press r to restart", True, (255, 255, 255))
        menu_text = font.render("press m to return to song select", True, (255, 255, 255))
        self.screen.blit(restart_text, (50, SCREEN_HEIGHT - 50))
        self.screen.blit(menu_text, (50, SCREEN_HEIGHT - 100))


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
        self.animation_played = False
        self.result_effects = False
        # Reset the start time to now
        self.start_time = time.time()
        
        self.load_assets()
        self.generate_notes()
        pygame.mixer.music.play()
        self.game_over = False  # Ensure the game_over flag is also reset
        pygame.mixer.music.play()
    
    def draw_progress_bar(self):
        font = pygame.font.Font(CUSTOM_FONT, 24)

        # Constants for appearance
        max_score = max(self.grade_thresholds.values())
        progress_bar_length = SCREEN_WIDTH - 500
        progress_bar_height = 20
        progress_bar_x = (SCREEN_WIDTH - progress_bar_length - 470)
        progress_bar_y = 40
        background_color = (0, 0, 0, 178)  # Adjusted for pygame's lack of direct RGBA support in draw.rect
        fill_color = BAR_COLOR  # Light purple
        marker_color = (255, 255, 255)  # White for grade markers

        # Constants for the banner background with shadow
        banner_height = 80  # Making the banner slightly taller than the progress bar for visual distinction
        banner_width = progress_bar_length + 50  # Including some extra width for the rectangle part of the banner
        triangle_extension = 40  # How far the triangle extends to the right of the rectangle
        shadow_offset = 7  # How far the shadow is offset from the original shape
        shadow_color = (10, 10, 10)  # Dark grey shadow color

        # Draw shadow for the rectangle part of the banner
        pygame.draw.rect(self.screen, shadow_color, (0, shadow_offset, banner_width + shadow_offset - 1, banner_height))

        shadow_offset -= 1
        # Draw shadow for the triangle part of the banner
        shadow_triangle_points = [
            (banner_width + shadow_offset, shadow_offset),  # Adjusted for shadow
            (banner_width + triangle_extension + shadow_offset, shadow_offset),  # Adjusted for shadow
            (banner_width + shadow_offset, banner_height - 1 + shadow_offset)  # Adjusted for shadow
        ]
        pygame.draw.polygon(self.screen, shadow_color, shadow_triangle_points)

        # Draw the rectangle part of the banner
        banner_color = (40, 40, 40)  # Original banner color
        pygame.draw.rect(self.screen, banner_color, (0, 0, banner_width, banner_height))

        # Draw the triangle part of the banner to create the extended effect
        triangle_points = [
            (banner_width, 0),  # Top right of the rectangle
            (banner_width + triangle_extension, 0),  # Point extending to the right
            (banner_width, banner_height - 1)  # Bottom right of the rectangle
        ]
        pygame.draw.polygon(self.screen, banner_color, triangle_points)

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
            if grade not in ["s", "f"]:
                pygame.draw.line(self.screen, marker_color, (marker_position, progress_bar_y), (marker_position, progress_bar_y + progress_bar_height), 1)
            
            # Display the grade letter above the marker
            grade_text = font.render(grade, True, marker_color)
            self.screen.blit(grade_text, (marker_position - grade_text.get_width() / 2, progress_bar_y - grade_text.get_height() - 5))

    def preprocess_lyrics(self, font, max_width, lyrics):
        self.processed_lyrics = []  # Store pre-processed lyrics as tuples of (start_time, [surfaces])
        for time_stamp, lyric in lyrics:
            wrapped_text = wrap_text(lyric, font, max_width)
            lyric_surfaces = [font.render(line, True, (255, 255, 255)) for line in wrapped_text]
            self.processed_lyrics.append((time_stamp, lyric_surfaces))

    def wrap_text(self, text, font, max_width):
        """
        Splits the text into lines that fit within a specified width, handling
        English, Japanese, and Korean text appropriately.
        """
        def is_asian_character(char):
            """Check if a character is Japanese or Korean."""
            return any([
                0x3040 <= ord(char) <= 0x30ff,  # Hiragana and Katakana
                0x4e00 <= ord(char) <= 0x9fff,  # CJK Unified Ideographs (common for Japanese Kanji and Chinese)
                0xac00 <= ord(char) <= 0xd7af,  # Hangul (Korean)
            ])

        lines = []
        current_line = ""
        words = text.split(' ')
        
        for word in words:
            if not word:  # Skip empty words
                continue
            if is_asian_character(word[0]):  # Check if the word starts with an Asian character
                for char in word:
                    test_line = current_line + char
                    test_surf = font.render(test_line, True, (255, 255, 255))
                    if test_surf.get_width() > max_width:
                        lines.append(current_line)
                        current_line = char
                    else:
                        current_line += char
                current_line += ' '  # Add space after the word if not at the start of a line
            else:  # Non-Asian, likely English or mixed, process by word
                test_line = current_line + word + ' '
                test_surf = font.render(test_line, True, (255, 255, 255))
                if test_surf.get_width() > max_width:
                    if current_line:  # If there's already content, start a new line
                        lines.append(current_line)
                        current_line = word + ' '
                    else:  # Word itself exceeds max width, force it on the line and split thereafter
                        lines.append(word + ' ')  # Ensure space is added to keep words separated
                else:
                    current_line += word + ' '
        
        if current_line:  # Add any remaining text as a new line
            lines.append(current_line)
        
        return lines
    
    def display_lyrics(self):
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Get current music time in seconds

        for i, (time_stamp, lyric_surfaces) in enumerate(self.processed_lyrics):
            # Check if it's time to display this set of lyrics
            if current_time >= time_stamp:
                if i == len(self.processed_lyrics) - 1 or current_time < self.processed_lyrics[i + 1][0]:
                    total_height_of_current_lyrics = sum(surface.get_height() for surface in lyric_surfaces)
                    y_offset = -(total_height_of_current_lyrics + 30)  # Adjust starting offset based on total height
                    for surface in lyric_surfaces:
                        # Calculate new y position for each line, starting from the bottom
                        y_position = SCREEN_HEIGHT + y_offset
                        self.screen.blit(surface, (20, y_position))
                        y_offset += surface.get_height()  # Adjust y_offset for the next line
                    break  # Exit the loop after displaying the current lyric
    
    def fade_to_black(self, fade_speed=10):
        fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 256, fade_speed):  # Increment by fade_speed
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(50)  # Adjust the delay for the desired speed of the fade effect

                
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart_game()
                    elif event.key == pygame.K_m and self.game_over:
                        # Transition back to song selection screen
                        pygame.mixer.music.stop()  # Stop any playing music
                        selected_song = song_select_screen(self.screen, self.font)  # Show song selection screen
                        self.__init__(selected_song, self.screen, self.font)  # Reinitialize the game with new song choice
                        return  # Exit the current game loop to start over with the new song

            if not pygame.mixer.music.get_busy() and not self.game_over:
                self.fade_to_black()
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
                self.display_lyrics()
            else:
                # self.screen.fill((0, 0, 0))  # Clear the screen
                self.display_results_screen()

            pygame.display.flip()
            self.clock.tick(60)