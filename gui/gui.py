import streamlit as st
from zipfile import ZipFile
import pandas as pd
import os

st.set_page_config(page_title="Vizual Analyzer", 
                    initial_sidebar_state="expanded",
                    menu_items={
                        'Report a bug': "https://github.com/bbennett80/30CES/",
                        'About': "A simple vizualizer of 30 CES samples."
                    }
                )

base_dir = "temp_directory"

def unzip_file(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(base_dir)

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
    st.image(spectrogram_file)
    st.audio(audio_file, autoplay=True)

uploaded_file = st.sidebar.file_uploader("Upload ZIP file", type="zip")

if uploaded_file is not None:
    unzip_file(uploaded_file)

    audio_dir = f"{base_dir}/audio"

    if os.path.exists(audio_dir):
        audio_files = sorted(os.listdir(audio_dir))
    else:
        audio_files = []
    
    selected_snippet = st.selectbox("Select Audio Snippet", audio_files)
    display_excel_data = st.sidebar.toggle("Show excel data")
    display_count_plot = st.sidebar.toggle("Show count plot")

    if selected_snippet:
        audio_path = os.path.join(audio_dir, selected_snippet)
        spectrogram_path = f"{base_dir}/spectrograms/{selected_snippet.replace('.wav', '.jpg')}"
        display_audio_and_spectrogram(audio_path, spectrogram_path)

    if display_excel_data:
        excel_file = find_excel_file(base_dir)
        df = pd.read_excel(excel_file)
        st.dataframe(df)

    if display_count_plot:
        count_plot = find_plot_file(base_dir)
        st.image(count_plot)
