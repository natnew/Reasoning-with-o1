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

st.title("Planning with O1")
st.write("This app demonstrates planning and task generation.")

goal = st.text_input("Enter your planning goal:")
if st.button("Generate Plan"):
    if goal:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Create a plan for the goal: {goal}"}]
        )
        st.markdown(f"### Generated Plan:\n\n{response.choices[0].message.content}")
    else:
        st.warning("Please enter a goal to generate a plan.")
