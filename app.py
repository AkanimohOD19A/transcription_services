import os
import glob
import whisper
import streamlit as st
from helper import save_record, create_spectogram, read_audio, record

## Function
def speech2Text(voicenote):
    model = whisper.load_model("small")
    result = model.transcribe(voicenote)

    outputnote = result["text"]

    return st.text(outputnote)


app_mode = st.sidebar.selectbox("Selections",
                                ['Transcribe', 'Synthesize'])

if app_mode == "Transcribe":
    ## Record and Save Audio
    st.header("Record your note")
    duration = st.number_input("Choose duration of recording", 3, 10, 5, 1) # Seconds
    filename = st.text_input("Enter a filename")

    if st.button(f"Click to Record"):
        if filename == "":
            st.warning("Please enter a filename")
        else:
            ## Start to record
            record_state = st.text("Recording..")
            fs = 48000
            myrecording = record(duration, fs)
            record_state.text(f"Saving sample as {filename}.mp3")

            ## Saving w/helper library
            path_of_recording = f"./samples/{filename}.mp3"

            save_record(path_of_recording, myrecording, fs)
            record_state.text(f"Done! Saved {filename}.mp3")

            ## Play Recording
            st.audio(read_audio(path_of_recording))

            ## Display Spectogram
            st.sidebar.text("Recorded Audio Spectogram")
            st.sidebar.markdown("---")
            fig = create_spectogram(path_of_recording)
            st.sidebar.pyplot(fig)

    ## Transcribe
    ## Display Transcription
    st.markdown("---")
    if st.checkbox("Transcribe Recording"):
        audio_folder = "samples"
        filenames = glob.glob(os.path.join(audio_folder, "*.mp3"))
        selected_filename = st.selectbox("Select a recording", filenames)
        with st.spinner("Generating your text..."):
            speech2Text(selected_filename)

if app_mode == "Synthesize":
    st.header("Synthesize Text with your voice.")

    st.markdown("An application that synthesizes your recording into written "
                "text, with promising possibilities for the vocally impaired")
    st.markdown("Work in Progress")