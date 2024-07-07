import os
import shutil

def organize_audio_files(source_dir):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    # Get all .wav files in the source directory
    wav_files = [f for f in os.listdir(source_dir) if f.endswith('.wav')]

    for file in wav_files:
        # Extract the scientific name from the file name
        parts = file.split('_')
        scientific_name = '_'.join(parts[2:-1])  # Join in case the scientific name has underscores

        # Create a directory for this scientific name if it doesn't exist
        target_dir = os.path.join(source_dir, scientific_name)
        os.makedirs(target_dir, exist_ok=True)

        # Move the file to the appropriate directory
        source_path = os.path.join(source_dir, file)
        target_path = os.path.join(target_dir, file)
        shutil.move(source_path, target_path)

    print("File organization complete.")

# Use the function
organize_audio_files('audio')