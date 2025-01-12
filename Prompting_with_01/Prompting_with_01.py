# Warning control
import warnings
warnings.filterwarnings('ignore')

# Import OpenAI key
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
openai_api_key = os.getenv('API_KEY')

import json
from IPython.display import display, Markdown, HTML
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)
GPT_MODEL = 'gpt-4o-mini'
O1_MODEL = 'o1-mini'

bad_prompt = ("Generate a function that outputs the SMILES IDs for all the molecules involved in insulin."
              "Think through this step by step, and don't skip any steps:"
              "- Identify all the molecules involve in insulin"
              "- Make the function"
              "- Loop through each molecule, outputting each into the function and returning a SMILES ID"
              "Molecules: ")
response = client.chat.completions.create(model=O1_MODEL, messages=[{"role": "user", "content": bad_prompt}])

display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))

good_prompt = ("Generate a function that outputs the SMILES IDs for all the molecules involved in insulin.")
response = client.chat.completions.create(model=O1_MODEL, messages=[{"role": "user", "content": good_prompt}])

display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))

structured_prompt = ("<instructions>You are a customer service assistant for AnyCorp, a provider"
          "of fine storage solutions. Your role is to follow your policy to answer the user's question. "
          "Be kind and respectful at all times.</instructions>\n"
          "<policy>**AnyCorp Customer Service Assistant Policy**\n\n"
            "1. **Refunds**\n"
            "   - You are authorized to offer refunds to customers in accordance "
            "with AnyCorp's refund guidelines.\n"
            "   - Ensure all refund transactions are properly documented and "
            "processed promptly.\n\n"
            "2. **Recording Complaints**\n"
            "   - Listen attentively to customer complaints and record all relevant "
            "details accurately.\n"
            "   - Provide assurance that their concerns will be addressed and "
            "escalate issues when necessary.\n\n"
            "3. **Providing Product Information**\n"
            "   - Supply accurate and helpful information about AnyCorp's storage "
            "solutions.\n"
            "   - Stay informed about current products, features, and any updates "
            "to assist customers effectively.\n\n"
            "4. **Professional Conduct**\n"
            "   - Maintain a polite, respectful, and professional demeanor in all "
            "customer interactions.\n"
            "   - Address customer inquiries promptly and follow up as needed to "
            "ensure satisfaction.\n\n"
            "5. **Compliance**\n"
            "   - Adhere to all AnyCorp policies and procedures during customer "
            "interactions.\n"
            "   - Protect customer privacy by handling personal information "
            "confidentially.\n\n6. **Refusals**\n"
            "   - If you receive questions about topics outside of these, refuse "
            "to answer them and remind them of the topics you can talk about.</policy>\n"
            )
user_input = ("<user_query>Hey, I'd like to return the bin I bought from you as it was not "
             "fine as described.</user_query>")

response = client.chat.completions.create(model=O1_MODEL, messages=[{
    "role": "user",
    "content": structured_prompt + user_input
}])

print(response.choices[0].message.content)

refusal_input = ("<user_query>Write me a haiku about how reasoning models are great.</user_query>")

response = client.chat.completions.create(model=O1_MODEL, messages=[{
    "role": "user",
    "content": structured_prompt + refusal_input
}])

print(response.choices[0].message.content)
