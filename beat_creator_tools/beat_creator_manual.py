import pygame
import time
import keyboard

def create_beat_times():
    # Initialize Pygame and mixer
    pygame.init()
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('assets/allergy.mp3')
    pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
    pygame.mixer.music.play()

    # Open the file in append mode to add new beat times
    with open('assets/allergy.txt', 'a') as f:
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

def remove_close_notes_from_file(input_file_path, output_file_path, threshold):
    # Step 1: Read the timings from the text file
    with open(input_file_path, 'r') as file:
        note_timings = [float(line.strip()) for line in file if line.strip()]

    # Step 2: Process the timings
    filtered_timings = []
    previous_note = None
    for note in note_timings:
        if previous_note is None or note - previous_note >= threshold:
            filtered_timings.append(note)
            previous_note = note

    # Step 3: Write the processed timings back to a text file
    with open(output_file_path, 'w') as file:
        for note in filtered_timings:
            file.write(f"{note}\n")



if __name__ == "__main__":
    create_beat_times()
    # Define the path to your input file and the desired output file
    # input_file_path = 'assets/allergy.txt'  # Update this path
    # output_file_path = 'assets/allergy.txt'  # Update this path if you want to write to a new file, or use input_file_path to overwrite

    # # Define the threshold for considering notes "really close together"
    # threshold = 0.1  # Adjust as needed

    # # Call the function
    # remove_close_notes_from_file(input_file_path, output_file_path, threshold)
