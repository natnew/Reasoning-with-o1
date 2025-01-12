# Securely load the API key from .env
from dotenv import load_dotenv
import os
import json

# Load the environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Context setup for simulation
context = {
    "inventory": {},
    "orders": [],
    "available_suppliers": [],
    "products": {},
    "suppliers": {},
    "production_capacity": {"immediate": 0, "next_week": 0},
    "shipping_options": {}
}

# Tools for reasoning and processing
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_new_orders",
            "description": "Fetches the list of new customer orders that have not been processed yet. There are no input parameters for this function.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_available_suppliers",
            "description": "This functions checks the list of available suppliers we can leverage for additional components.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Fetches the product details included the required components necessary for creating more of the product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product.",
                    }
                },
                "required": ["product_id"],
                "additionalProperties": False,
            },
        },
    },
    # More functions are defined similarly, handling various aspects like stock allocation,
    # supplier information, placing purchase orders, production scheduling, and shipping.
]

# Function Definitions
def get_inventory_status(product_id):
    quantity = context['inventory'].get(product_id, 0)
    return {'product_id': product_id, 'quantity': quantity}

def get_product_details(product_id):
    product = context['products'].get(product_id, {})
    return {"name": product.get('name', ''), "components_needed": product.get("components_needed", {})}

def update_inventory(product_id, quantity_change):
    if product_id not in context['inventory']:
        return {'error': f"Product ID {product_id} not found in inventory."}
    new_quantity = context['inventory'][product_id] + int(quantity_change)
    if new_quantity < 0:
        return {'error': 'Resulting inventory cannot be negative.'}
    context['inventory'][product_id] = new_quantity
    return {'product_id': product_id, 'new_quantity': new_quantity}

def fetch_new_orders():
    return context['orders'][0]

# Other similar functions for managing supplier interactions, production capacity, and order processing.

# Mapping function names to actual functions
function_mapping = {
    'get_inventory_status': get_inventory_status,
    'get_product_details': get_product_details,
    'update_inventory': update_inventory,
    'fetch_new_orders': fetch_new_orders,
    # Map all other functions defined earlier
}

# High-level process handling
def process_scenario(scenario):
    append_message({'type': 'status', 'message': 'Generating plan...'})
    plan = call_o1(scenario)
    append_message({'type': 'plan', 'content': plan})
    append_message({'type': 'status', 'message': 'Executing plan...'})
    messages = call_gpt4o(plan)
    append_message({'type': 'status', 'message': 'Processing complete.'})
    return messages

def append_message(message):
    message_type = message.get('type', '')
    if message_type == 'status':
        print(message['message'])
    elif message_type == 'plan':
        print("\nPlan:\n", message['content'])
    elif message_type == 'assistant':
        print("\nAssistant:\n", message['content'])
    elif message_type == 'function_call':
        print(f"\nFunction call: {message['function_name']} with arguments {message['arguments']}")
    elif message_type == 'function_response':
        print(f"\nFunction response for {message['function_name']}: {message['response']}")

def call_o1(scenario):
    prompt = f"""{o1_prompt}\n\nScenario:\n{scenario}\n\nPlease provide the next steps in your plan."""
    response = client.chat.completions.create(model=O1_MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response.choices[0].message.content

def call_gpt4o(plan):
    gpt4o_policy_prompt = gpt4o_system_prompt.replace("{policy}", plan)
    messages = [{'role': 'system', 'content': gpt4o_policy_prompt}]
    # Handling logic for GPT-4O integration
    # Looping to manage tool calls, assistant messages, and more

# Example usage
scenario_text = (
    "We just received a major shipment of new orders. "
    "Please generate a plan that gets the list of awaiting "
    "orders and determines the best policy to fulfill them.\n\n"
    "The plan should include checking inventory, ordering "
    "necessary components from suppliers, scheduling production "
    "runs with available capacity, ordering new components "
    "required from suppliers, and arranging shipping to the "
    "retailer’s distribution center in Los Angeles. Notify "
    "the customer before completing.\n\n"
    "Prioritize getting any possible orders out that you can "
    "while placing orders for any backlog items."
)

# Process the scenario
messages = process_scenario(scenario_text)
for x in messages:
    print(x)
