import librosa
import numpy as np

def simplify_beat_times(beat_times, n=4):
    """
    Simplify the beat timings by selecting every nth beat.
    
    :param beat_times: Array of beat times.
    :param n: Interval of beats to select.
    :return: Simplified array of beat times.
    """
    return beat_times[::n]

def main():
    # Path to your song
    song_path = 'allergy.mp3'
    
    # Load the audio file
    y, sr = librosa.load(song_path)
    
    # Perform beat detection
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    # Simplify the beat times to reduce note clutter
    simplified_beat_times = simplify_beat_times(beat_times, n=4)  # Adjust 'n' as needed
    
    print("Simplified beat times in seconds:")
    print(simplified_beat_times)
    
    # Optionally, save the simplified beat times to a file
    np.savetxt('simplified_beat_times.txt', simplified_beat_times, fmt='%0.6f')

if __name__ == '__main__':
    main()
