import librosa
import numpy as np

def save_onset_times_to_file(audio_file_path, output_txt_path):
    # Load your audio file
    y, sr = librosa.load(audio_file_path, sr=None)

    # Separate harmonic component for clearer pitch analysis
    y_harmonic, _ = librosa.effects.hpss(y)

    # Detect onsets based on onset strength
    o_env = librosa.onset.onset_strength(y=y_harmonic, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    # Convert onset frames to time
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Save the onset times to a text file
    with open(output_txt_path, 'w') as f:
        for time in onset_times:
            f.write(f"{time}\n")

    print(f"Onset timings saved to {output_txt_path}")

# Example usage
audio_file_path = 'assets/ima/ima.mp3'  # Update this path to your audio file
output_txt_path = 'assets/ima/ima2.txt'  # Specify where you'd like to save the timings

save_onset_times_to_file(audio_file_path, output_txt_path)
