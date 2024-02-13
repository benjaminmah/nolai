import pygame
import time
import keyboard

def create_beat_times():
    # Initialize Pygame and mixer
    pygame.init()
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('allergy.mp3')
    pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
    pygame.mixer.music.play()

    # Open the file in append mode to add new beat times
    with open('beat_times.txt', 'a') as f:
        print("Press SPACE to add beat time. Press Q to quit.")
        
        # Start time
        start_time = time.time()
        
        # Infinite loop to capture user input
        while True:
            # Check if SPACE key is pressed
            if keyboard.is_pressed('space'):
                # Calculate the beat time relative to the start time
                beat_time = time.time() - start_time
                
                # Write the beat time to the file
                f.write(f"{beat_time}\n")
                print(f"Beat time added: {beat_time}")
                
            # Check if Q key is pressed
            if keyboard.is_pressed('q'):
                # Stop the music and exit the loop
                pygame.mixer.music.stop()
                print("Beat times recording finished.")
                return
              
            # Add a small delay to prevent high CPU usage
            time.sleep(0.05)
                
    # Stop the music
    pygame.mixer.music.stop()

if __name__ == "__main__":
    create_beat_times()
