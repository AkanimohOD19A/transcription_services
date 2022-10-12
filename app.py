import whisper
import streamlit as st
from helper import save_record, create_spectogram, read_audio, record

## Function
def speech2Text(voicenote):
    model = whisper.load_model("small")
    result = model.transcribe(voicenote)

    outputnote = result["text"]

    return st.text(outputnote)


app_mode = st.sidebar.selectbox()['Transcribe', 'Synthesize']

if app_mode == "Transcribe":
    ## Record and Save Audio
    st.header("Record your note")
    filename = st.text_input("Enter a filename")
    duration = st.select_slider("Choose duration of recording", 3, 5, 10, 1) #Seconds

    if st.button(f"Click to Record"):
        if filename == "":
            st.warning("Choose a filename")
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
            fig = create_spectogram(path_of_recording)
            st.pyplot(fig)

            ## Display Transcription
            speech2Text(path_of_recording)

    ## Transcribe


if app_mode == "Synthesize":
    st.header("Synthesize Text with your voice.")