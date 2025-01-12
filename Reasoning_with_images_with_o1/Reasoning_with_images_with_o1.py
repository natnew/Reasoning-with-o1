# Warning control
import warnings
warnings.filterwarnings('ignore')

import json
from openai import OpenAI
from IPython.display import display, Markdown, Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('API_KEY')

client = OpenAI(api_key=openai_api_key)

GPT_MODEL = 'gpt-4o-mini'
O1_MODEL = 'o1'

# Image file path
image_filepath = 'data/org_chart_sample.png'

# Display the image
display(Image(image_filepath))

# Function to encode an image in Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# O1 Vision helper function
def o1_vision(file_path, prompt, model, json_mode=False):
    base64_image = encode_image(file_path)

    if json_mode:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            response_format={"type": "json_object"}
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ]
        )
    return response

# Query the model with a general question
response = o1_vision(
    file_path=image_filepath,
    prompt='What is this?',
    model=O1_MODEL
)

display(Markdown(response.choices[0].message.content))

# Structured prompt for extracting org hierarchy
structured_prompt = (
    "<instructions>You are a consulting assistant who processes org data. "
    "Extract the org hierarchy from the image you're provided in a structured format. "
    "The structure should be returned in JSON containing:\n"
    "- arbitrary ID of the person that you can generate\n"
    "- name of the person\n"
    "- role of the person\n"
    "- an array of IDs they report to\n"
    "- an array of IDs that report to them"
    "</instructions>"
)

# Query the model for structured data
o1_response = o1_vision(
    file_path=image_filepath,
    model='o1',
    prompt=structured_prompt,
    json_mode=True
)

print(o1_response.choices[0].message.content)

# Parse and clean the JSON response
cleaned_json = o1_response.choices[0].message.content.replace('```json', '').replace('```', '')
org_data = json.loads(cleaned_json)
org_data

# Analysis prompt for further questions
analysis_prompt = (
    "<instructions>You are an org chart expert assistant. Your role is to"
    "answer any org chart questions with your org data.</instructions>\n"
    f"<org_data>{org_data}</org_data>\n"
)

# Example question about the org data
messages = [{
    "role": "user",
    "content": analysis_prompt + "<question>Who has the highest ranking reports, and which manager has the most reports?</question>"
}]

response = client.chat.completions.create(model=O1_MODEL, messages=messages)

display(Markdown(response.choices[0].message.content))

# Display another image for analysis
image_filepath = 'data/erd-relation-order.png'
display(Image(image_filepath))
