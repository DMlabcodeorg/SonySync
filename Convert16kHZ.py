import os
import sys
import glob
from pydub import AudioSegment


def convert_wav_files_to_16khz(original_path):
    # Check if the path exists
    if not os.path.exists(original_path):
        print(f"Path not found: {original_path}")
        return

    # Create new directory to save the converted files
    new_path = os.path.join(original_path, "_16kHZ")
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Find all .wav files under the given path
    for filepath in glob.iglob(original_path + '**/*.wav', recursive=True):
        # Read the .wav file
        audio = AudioSegment.from_wav(filepath)

        # Check if the audio is already 16kHz
        if audio.frame_rate == 16000:
            print(f"Audio file {filepath} is already at 16kHz.")
            continue

        # Convert the audio file to 16kHz
        audio = audio.set_frame_rate(16000)

        # Extract the filename and the extension from the path
        filename = os.path.basename(filepath)

        # Save the 16kHz audio to the new path with the original filename
        audio.export(os.path.join(new_path, filename), format="wav")

        print(f"Converted: {filepath} to 16kHz.")


def main():
    # Check if the path is provided
    if len(sys.argv) < 2:
        print("Usage: python Convert16kHZ.py <path_to_scan_and_convert_to_16kHZ>")
        sys.exit(1)

    path_to_scan = sys.argv[1]
    convert_wav_files_to_16khz(path_to_scan)


if __name__ == "__main__":
    main()
