import streamlit as st
from openai import OpenAI
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit Sidebar
st.sidebar.title("OpenAI API Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
if not api_key:
    st.sidebar.warning("Please enter your OpenAI API key.")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("Reasoning with Images with O1")
st.write("This app performs reasoning based on images.")

uploaded_image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

if st.button("Analyse Image"):
    if uploaded_image:
        image_bytes = uploaded_image.read()
        encoded_image = BytesIO(image_bytes).getvalue()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Analyse this image."},
                {"type": "image", "image_url": encoded_image}
            ]
        )
        st.markdown(f"### Image Analysis:\n\n{response.choices[0].message.content}")
    else:
        st.warning("Please upload an image to analyse.")
