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

st.title("Meta-prompting with O1")
st.write("This app uses meta-prompting to refine instructions.")

instructions = st.text_area("Enter initial instructions:")
eval_results = st.text_area("Paste evaluation results (JSON format):")

if st.button("Refine Instructions"):
    if instructions and eval_results:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Refine these instructions:\n{instructions}\n\nResults:\n{eval_results}"}]
        )
        st.markdown(f"### Refined Instructions:\n\n{response.choices[0].message.content}")
    else:
        st.warning("Please enter both instructions and evaluation results.")
