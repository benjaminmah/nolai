import librosa
import numpy as np

# Load an audio file as a waveform `y`
# Here, `sr` is the sampling rate
y, sr = librosa.load('assets/girlscapitalism.mp3', sr=None)

# Perform beat tracking
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)

print("Beat Times:", beat_times)

# Assuming `beat_times` contains the list of beat times from your code
with open('assets/girlscapitalism2.txt', 'w') as file:
    for beat_time in beat_times:
        file.write(f"{beat_time}\n")

print("Beat times have been stored")