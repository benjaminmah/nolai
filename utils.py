import pygame

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

def wrap_text(text, font, max_width):
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

def preprocess_lyrics(font, max_width, lyrics):
    processed_lyrics = []  # Store pre-processed lyrics as tuples of (start_time, [surfaces])
    for time_stamp, lyric in lyrics:
        wrapped_text = wrap_text(lyric, font, max_width)
        lyric_surfaces = [font.render(line, True, (255, 255, 255)) for line in wrapped_text]
        processed_lyrics.append((time_stamp, lyric_surfaces))
    return processed_lyrics


def threshold_calculator(file_path):
    threshold = {}

    perfect_score = 0
    good_score = 0
    okay_score = 0

    # count the number of notes
    with open(file_path, 'r') as file:
        line_count = 0
        for line in file:
            line_count += 1
            perfect_score += min(100 + (line_count * 10) // 2, 350)
            good_score += min(50 + (line_count * 10) // 2, 350)
            okay_score += min(10 + (line_count * 10) // 2, 350)

    # calculate the max score possible (all perfect streak)
            
    # top 5% is s
    threshold['s'] = perfect_score - perfect_score * 0.05

    # top 10% is a
    threshold['a'] = perfect_score - perfect_score * 0.10

    # top 20% is b
    threshold['b'] = perfect_score - perfect_score * 0.20

    # top 35% is c
    threshold['c'] = perfect_score - perfect_score * 0.35

    # top 55% is d
    threshold['d'] = perfect_score - perfect_score * 0.55

    # f is fail
    threshold['f'] = 0

    print(threshold)
    return threshold

threshold_calculator("assets/allergy/allergy.txt")