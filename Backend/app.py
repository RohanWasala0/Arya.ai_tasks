import streamlit as st

uploaded_file = st.file_uploader(label="Upload an image", type=["jpg", "png"])
if uploaded_file:
    st.image(uploaded_file)
