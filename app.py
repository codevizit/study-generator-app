# app.py

import streamlit as st
from logic import generate_notes, generate_quiz, generate_summary, generate_flashcards

st.set_page_config(page_title="Study Helper", layout="centered")

st.title("📘 Study Helper: Generate Notes, Quiz, Flashcards & Summary")

user_input = st.text_area("✍️ Paste your study content below:", height=300)

if user_input.strip():

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Generate Notes"):
            with st.spinner("Generating notes..."):
                try:
                    notes = generate_notes(user_input)
                    st.success("Done!")
                    st.markdown("### 📝 Notes")
                    st.write(notes)
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        if st.button("❓ Generate Quiz"):
            with st.spinner("Generating quiz..."):
                try:
                    quiz = generate_quiz(user_input)
                    st.success("Done!")
                    st.markdown("### ❓ Quiz")
                    st.write(quiz)
                except Exception as e:
                    st.error(f"Error: {e}")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🧠 Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                try:
                    flashcards = generate_flashcards(user_input)
                    st.success("Done!")
                    st.markdown("### 🧠 Flashcards")
                    for fc in flashcards:
                        st.markdown(f"**{fc.term}**: {fc.definition}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col4:
        if st.button("📄 Generate Summary"):
            with st.spinner("Generating summary..."):
                try:
                    summary = generate_summary(user_input)
                    st.success("Done!")
                    st.markdown("### 📄 Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("Enter study text above to get started.")
