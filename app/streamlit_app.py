import streamlit as st
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.speech_to_text import record_and_transcribe, start_background_recording, transcribe_all
from src.excel_utils import load_csv, update_review, save_csv

DATA_PATH = "data/drugs.csv"
st.title("💊 Voice Review Updater")
df = load_csv(DATA_PATH)

# Input ID
unique_id = st.text_input("Enter Customer Unique ID")

if unique_id:
    try:
        row = df[df["uniqueID"] == int(unique_id)]
        if not row.empty:
            st.subheader("📄 Customer Record:")
            st.dataframe(row)
        else:
            st.warning("ID not found.")
    except ValueError:
        st.error("Please enter a valid number")

# Init session state
if "listening" not in st.session_state:
    st.session_state.listening = False
if "stop_fn" not in st.session_state:
    st.session_state.stop_fn = None
if "review_text" not in st.session_state:
    st.session_state.review_text = ""

# Start button
if st.button("🎙 Start Listening") and not st.session_state.listening:
    st.session_state.stop_fn = start_background_recording()
    st.session_state.listening = True
    st.success("🔴 Listening... Press 'Stop' to finish")

# Stop button
if st.button("⏹ Stop Listening") and st.session_state.listening:
    st.session_state.stop_fn(wait_for_stop=False)
    st.session_state.listening = False
    st.success("✅ Recording stopped. Transcribing...")
    text = transcribe_all()
    st.session_state.review_text = text

# Show transcribed text
if st.session_state.review_text:
    st.subheader("📝 Transcribed Review:")
    st.success(st.session_state.review_text)

    if st.button("🔁 Re-record"):
        st.session_state.review_text = ""

    if st.button("✅ Confirm and Save Review"):
        df = update_review(df, unique_id, st.session_state.review_text)
        save_csv(df, DATA_PATH)
        st.success("✅ Review saved successfully.")
