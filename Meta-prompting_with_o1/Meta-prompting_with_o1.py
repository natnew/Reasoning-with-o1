# Securely load environment variables
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from IPython.display import display, Markdown
import pandas as pd
from matplotlib import pyplot as plt

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('API_KEY')

client = OpenAI(api_key=openai_api_key)

# Function to handle token calculation
def num_tokens_from_messages(messages):
    entire_input = ""
    for message in messages:
        entire_input += message["content"] + " "
    tokens = encoding.encode(entire_input)
    return len(tokens)

# Function for processing policy updates
def evaluate_function_calls(df, policy, model, i=0, verbose=False):
    records = []
    for row_number, row in df.iterrows():
        record = process_row(row_number, row, policy, model, i, verbose)
        records.append(record)

    df = pd.DataFrame(records)
    df["cleaned_transcript"] = df["transcript"].apply(filter_messages)
    total_accuracy = df["is_correct"].mean()
    return df, total_accuracy

# Extract routine and results
routines = [flight_cancellation_routine]
results = []
accuracies = []

# Simulation for multiple evaluations
for i in range(3):
    display(Markdown(f"## Iteration {i + 1}"))
    
    eval_df = pd.read_csv('evals/policyEvals.csv')
    df, accuracy = evaluate_function_calls(eval_df, flight_cancellation_routine, GPT_MODEL, i)
    accuracies.append(round(accuracy * 100, 2))
    results.append(df)
    display(Markdown(f"### Accuracy: {accuracy:.2%}"))
    
    failed_ids = df[df["is_correct"] == False].index.tolist()
    display(df.loc[failed_ids])

# Plot accuracy improvements over iterations
plt.plot(range(1, len(accuracies) + 1), accuracies, marker='o')
plt.title("Accuracy over Runs")
plt.xlabel("Run Number")
plt.ylabel("Accuracy (%)")
plt.show()

# Identify the best routine
best_routine = routines[accuracies.index(max(accuracies))]
display(Markdown(f"## Best Routine:\n{best_routine}"))
