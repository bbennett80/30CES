import streamlit as st

from zipfile import ZipFile
import pandas as pd
import os


def unzip_file(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("temp_directory")

def find_excel_file(directory):
    for file in os.listdir(directory):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            return os.path.join(directory, file)
    return None

def find_plot_file(directory):
    for file in os.listdir(directory):
        if file.endswith('.png'):
            return os.path.join(directory, file)
    return None

def display_audio_and_spectrogram(audio_file, spectrogram_file):
    image = st.image(spectrogram_file)
    audio = st.audio(audio_file, autoplay=True)
    return image, audio

audio_dir = "temp_directory/audio"
audio_files = os.listdir(audio_dir) if os.path.exists(audio_dir) else []

uploaded_file = st.sidebar.file_uploader("Upload ZIP file", type="zip")
selected_snippet = st.selectbox("Select Audio Snippet", audio_files)
display_excel_data = st.sidebar.toggle("Show excel data")
display_count_plot = st.sidebar.toggle("Show count plot")

if uploaded_file is not None:
    unzip_file(uploaded_file)

if selected_snippet:
    audio_path = os.path.join(audio_dir, selected_snippet)
    spectrogram_path = f"temp_directory/spectrograms/{selected_snippet.replace('.wav', '.jpg')}"
    display_audio_and_spectrogram(audio_path, spectrogram_path)

if display_excel_data:
    excel_data_path = "temp_directory/"
    excel_file = find_excel_file(excel_data_path)
    df = pd.read_excel(excel_file)
    st.dataframe(df)

if display_count_plot:
    plot_path = "temp_directory/"
    count_plot = find_plot_file(plot_path)
    st.image(count_plot)
