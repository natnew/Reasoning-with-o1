import streamlit as st
from openai import OpenAI
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

st.title("Coding with O1")
st.write("This app demonstrates code generation with O1.")

prompt = st.text_area("Enter your code generation prompt:")

if st.button("Generate Code"):
    if prompt:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        st.code(response.choices[0].message.content)
    else:
        st.warning("Please enter a prompt to generate code.")
