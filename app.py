import streamlit as st
import os
import subprocess

# Set the page configuration
st.set_page_config(page_title="Reasoning with o1", layout="wide")

# Sidebar for OpenAI API Key
st.sidebar.title("Reasoning with o1")
st.sidebar.write("Learn how to use and prompt OpenAI's o1 model.")
st.sidebar.info("Coding, Meta-prompting, Planning, Prompting, and Reasoning with the o1 model.")
st.sidebar.title("API Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

if not api_key:
    
    st.sidebar.warning("Please enter your OpenAI API key to proceed.")
    st.stop()

# Model Selection
st.sidebar.title("Model Selection")
models = {
    "GPT-4o-mini_MODEL": "gpt-4o-mini",
    "o1-mini_MODEL": "o1-mini"
}
model_selection = st.sidebar.selectbox("Select the model:", list(models.keys()))
selected_model = models[model_selection]

# Dropdown for project selection
st.title("Reasoning with o1")

project_options = [
    "Coding_with_o1",
    "Meta-prompting_with_o1",
    "Planning_with_o1",
    "Prompting_with_01",
    "Reasoning_with_images_with_o1"
]

selected_project = st.selectbox("Select a project to run:", project_options)

# Run the selected project's app.py
if st.button("Run Selected Project"):
    project_path = os.path.join(os.getcwd(), selected_project, "app.py")

    if os.path.exists(project_path):
        try:
            # Set the API key and selected model as environment variables
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["SELECTED_MODEL"] = selected_model

            # Execute the selected project's app.py
            subprocess.run(["streamlit", "run", project_path], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred while running {selected_project}: {e}")
    else:
        st.error(f"Could not find app.py in the selected project folder: {selected_project}.")
