
import streamlit as st
import os
import zipfile
from datetime import datetime
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
import matplotlib.pyplot as plt
import pandas as pd

st.title("BirdNET Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload audio file", type=["wav", "mp3", "flac"])

base_dir = 'content'
extractions_dir = os.path.join(base_dir, 'audio')
spectrograms_dir = os.path.join(base_dir, 'spectrograms')


def directory_setup(extractions_dir, spectrograms_dir):
    # Check if 'contnet' directory exists, create it if not
    if not os.path.exists(base_dir):
        os.makedirs(extractions_dir)

    # Check if 'audio' directory exists, create it if not
    if not os.path.exists(extractions_dir):
        os.makedirs(extractions_dir)

    # Check if 'spectrograms' directory exists, create it if not
    if not os.path.exists(spectrograms_dir):
        os.makedirs(spectrograms_dir)


def uploaded_file_base(uploaded_file):
    return uploaded_file.name.split(".")[0]

# Generate Dataframe and save to excel.
def generate_detections(analyzer, uploaded_file, min_conf, extractions_dir, spectrograms_dir):
    recording = Recording(analyzer, uploaded_file, min_conf)
    recording.analyze()

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

    st.toast(f"Detected {len(detected_table)} samples in {uploaded_file}")

    df = pd.DataFrame(
        data=detected_table,
        columns=['Common Name', 'Sci Name', 'Detection Timestamp (s)', 'Confidence', 'Audio File', 'Spectrogram']
    )

    df.to_excel(f"content/{uploaded_file_base}_detections.xlsx", index=False)

    st.toast("Preparing detections audio.")
    recording.extract_detections_as_audio(
        directory = extractions_dir,
        format = audio_format,
        bitrate = "192k",
        min_conf = min_conf,
        padding_secs = padding_secs
    )

    # Extract to spectrograms from detections
    st.toast("Preparing detections spectrograms.")
    recording.extract_detections_as_spectrogram(
        directory = spectrograms_dir,
        padding_secs = padding_secs,
        min_conf = min_conf,
        top = 14000,
        format = spectrogram_format,
        dpi = dpi
    )


# Calculate counts and average confidence
def generate_counts_plot(df):
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
                f'{avg_conf:.1%}', ha='center', va='bottom',
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
def create_zip():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    zip_filename = f"{uploaded_file_base}_{timestamp}_result.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, base_dir))



if __name__ == "__main__":
    analyzer = Analyzer()


    if uploaded_file:
        # Sets some default variables
        min_conf = st.sidebar.number_input("Mininum Model Confidence", 
                                    min_value=0.00, 
                                    max_value=1.0,
                                    value=0.70,
                                    step=0.01,
                                    help="Literature suggest a Confidence of 0.7",
                                    key="min_conf"
                                )

        padding_secs = st.sidebar.number_input("Padding, seconds",
                                        min_value=0.00, 
                                        max_value=3.0,
                                        value=2.0,
                                        step=0.1,
                                        help="Default padding is 2s.",
                                        key="padding_secs"
                                    )

        dpi = st.sidebar.number_input("Graph Dots Per Inch (dpi)",
                                min_value=144,
                                max_value=1080,
                                value=1080,
                                step=10,
                                help="More dpi will result in a larger, more detailed plot.",
                                key="dpi"
                            )

        audio_format = st.sidebar.selectbox("Detected audio ouput format",
                                    options=["wav", "mp3", "flac"],
                                    key="audio_format"
                                )

        spectrogram_format = st.sidebar.selectbox("Spectrogram output format",
                                        options=["jpg", "png"],
                                        )


        process_audio = st.sidebar.button("Process audio")
        if process_audio:
            # directory_setup(extractions_dir, spectrograms_dir)
            uploaded_file_base = uploaded_file_base(uploaded_file)
            with st.status(f"Processing {uploaded_file_base}"):
                generate_detections(analyzer, str(uploaded_file.read()), min_conf, extractions_dir, spectrograms_dir)
