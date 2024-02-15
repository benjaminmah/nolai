import random

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
    
    # Step 3: Add duplicate notes
    for index in range(len(filtered_timings)-1, -1, -1):
        if (len(filtered_timings) - index) % random.randint(5, 20) == 0:
            filtered_timings.insert(index+1, filtered_timings[index])

    # Step 4: Write the processed timings back to a text file
    with open(output_file_path, 'w') as file:
        for note in filtered_timings:
            file.write(f"{note}\n")

# Define the path to your input file and the desired output file
input_file_path = 'assets/allergy/allergy.txt'  # Update this path
output_file_path = 'assets/allergy/allergy2.txt'  # Update this path if you want to write to a new file, or use input_file_path to overwrite

# Define the threshold for considering notes "really close together"
threshold = 0.1  # Adjust as needed

# Call the function
remove_close_notes_from_file(input_file_path, output_file_path, threshold)
