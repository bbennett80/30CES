import os
import zipfile
from datetime import datetime
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
import matplotlib.pyplot as plt
import pandas as pd

base_dir = 'content'
extractions_dir = os.path.join(base_dir, 'audio')
spectrograms_dir = os.path.join(base_dir, 'spectrograms')

uploaded_file = input("Please enter the file to analyze: ")
uploaded_file_base = uploaded_file.split(".")[0]

# Check if 'content' directory exists, create it if not
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Check if 'audio' directory exists, create it if not
if not os.path.exists(extractions_dir):
    os.makedirs(extractions_dir)

# Check if 'spectrograms' directory exists, create it if not
if not os.path.exists(spectrograms_dir):
    os.makedirs(spectrograms_dir)

# Sets some default variables
min_conf = 0.7
padding_secs = 1.0
dpi = 144
audio_format = 'wav'
spectrogram_format = 'jpg'

# Initializes Recording and Analyzer
analyzer = Analyzer()
recording = Recording(analyzer, uploaded_file, min_conf=min_conf)
recording.analyze()

# Generate Dataframe and save to excel.
detections = recording.detections
detected_table = []

for detection in detections:
    row = []
    start = int(detection['start_time']) - int(padding_secs)
    finish = int(detection['end_time']) + int(padding_secs)

    common_name = detection['common_name']
    scientific_name = detection['scientific_name']
    time_frame = f"{start}-{finish}"
    confidence = detection['confidence']
    audio_file = f"{uploaded_file_base}_{time_frame}.{audio_format}"
    spectrogram = f"{uploaded_file_base}_{time_frame}.{spectrogram_format}"

    row.append(common_name)
    row.append(scientific_name)
    row.append(time_frame)
    row.append("{0:.1%}".format(confidence))
    row.append(audio_file)
    row.append(spectrogram)
    print(f"{common_name} ({scientific_name}): {confidence:.1%}")
    detected_table.append(row)

print(f"Detected {len(detected_table)} samples in {uploaded_file}")

df = pd.DataFrame(
    data=detected_table,
    columns=['Common Name', 'Sci Name', 'Detection Timestamp (s)', 'Confidence', 'Audio File', 'Spectrogram']
)

df.to_excel(f"content/{uploaded_file_base}_detections.xlsx", index=False)

# Extract to .mp3 audio files, only if confidence is > `min_conf` with `padding_secs` seconds of audio padding.
print("Preparing audio and spectrogram extractions...")
recording.extract_detections_as_audio(
    directory = extractions_dir,
    format = audio_format,
    bitrate = "192k",
    min_conf = min_conf,
    padding_secs = padding_secs
)

# # Extract to spectrograms from detections
recording.extract_detections_as_spectrogram(
    directory = spectrograms_dir,
    padding_secs = padding_secs,
    min_conf = min_conf,
    top = 14000,
    format = spectrogram_format,
    dpi = dpi
)

# Calculate counts and average confidence
name_counts = df['Sci Name'].value_counts()
avg_confidence = df.groupby('Sci Name')['Confidence'].apply(lambda x: pd.to_numeric(x.str.rstrip('%')).mean())

# Plotting
plt.figure(figsize=(14, 8))  # Increased figure size
bars = name_counts.plot(kind='bar', color='skyblue')

# Add average Confidence text above each bar
for bar, avg_conf in zip(bars.patches, avg_confidence):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5,
             f'{avg_conf:.2f}%', ha='center', va='bottom',
             rotation=0, fontsize=8)

plt.title('Count: Sci Name Detections with Mean Model Confidence')
plt.xlabel('Sci Name')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')

# Increase top margin to accommodate labels
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# Increase y-axis limit to make room for labels
plt.ylim(0, plt.ylim()[1] * 1.1)  # Increase the upper limit by 10%

plt.savefig(f'content/{uploaded_file_base}_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Walk through the 'content' directory and add all files and directories to the zip archive for download
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
zip_filename = f"{uploaded_file_base}_{timestamp}_result.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, base_dir))
