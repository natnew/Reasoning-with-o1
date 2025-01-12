import streamlit as st
from openai import OpenAI
import os
import json

# Fetch API Key and Selected Model from Environment Variables
api_key = os.getenv("OPENAI_API_KEY")
selected_model = os.getenv("SELECTED_MODEL")

if not api_key or not selected_model:
    st.error("API Key or Model Selection is missing. Please run from the main app.")
    st.stop()

# Initialize OpenAI Client
client = OpenAI(api_key=api_key)

# Load Approaches from JSON File
def load_approaches(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("The approaches.json file is missing.")
        st.stop()
    except json.JSONDecodeError:
        st.error("The approaches.json file is invalid.")
        st.stop()

# Load prompt approaches
approaches = load_approaches("approaches.json")

# Sidebar for Approach Selection
st.sidebar.title("Approach Selection")
approach_selection = st.sidebar.selectbox("Select the approach:", list(approaches.keys()))
selected_prompt = approaches[approach_selection]

# Display Selected Configuration
st.title("Prompting with O1")
st.write(f"Using model: `{selected_model}`")
st.write(f"Approach: `{approach_selection}`")
st.markdown(f"### Selected Prompt:\n\n{selected_prompt}")

# Generate Response
if st.button("Generate Response"):
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": selected_prompt.strip()}]
        )
        st.markdown("### Response:")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occurred: {e}")
