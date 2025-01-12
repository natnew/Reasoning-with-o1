# Warning control
import warnings
warnings.filterwarnings('ignore')

# Import OpenAI key
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('API_KEY')

from IPython.display import display, Image, Markdown
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)
GPT_MODEL = 'gpt-4o-mini'
O1_MODEL = 'o1-mini'

def get_chat_completion(model, prompt):
    """
    Calls the OpenAI API to get a chat completion.

    :param model: The model to use for the completion.
    :param prompt: The prompt to send to the model.
    :return: The completion response from the model.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

react_demo_prompt = """Create an elegant, delightful React component for an Interview Feedback Form where:

1. The interviewer rates candidates across multiple dimensions using rubrics
2. Each rating must include specific evidence/examples
3. The final recommendation should auto-calculate based on a weighted scoring system
4. The UI should guide interviewers to give specific, behavioural feedback

The goal is to enforce structured, objective feedback gathering. A smart model should:
- Create a thoughtful rubric structure
- Add helpful prompts/placeholders
- Build in intelligent validation

Make sure to
 - Call the element FeedbackForm
 - Start the code with "use client"

Respond with the code only! Nothing else!"""

gpt_code = get_chat_completion(GPT_MODEL, react_demo_prompt)

print(gpt_code)

display(Image('gpt4_app_image.png'))

o1_code = get_chat_completion(O1_MODEL, react_demo_prompt)

print(o1_code)

display(Image('o1_app_image.png'))

# Pre-generated code snippet with issues that need to be resolved.
code_snippet = """
def process_orders(orders_list, settings={}, debug=False, notify_customer=True):
    results = []
    errors = []
    notifications = []
    # Process all orders
    for i in range(0, len(orders_list)):
        # Get order
        order = orders_list[i]
        try:
            # Validate order has required fields
            if 'id' in order and 'items' in order and 'customer' in order:
                # Check customer info
                if 'email' in order['customer'] and 'name' in order['customer']:
                    # Validate items
                    items_valid = True
                    total = 0
                    # Check each item
                    for item in order['items']:
                        if not ('product_id' in item and 'quantity' in item):
                            items_valid = False
                            errors.append(f"Invalid item in order {order['id']}")
                            if debug:
                                print(f"Debug: Invalid item found in order {order['id']}")
                        else:
                            # Calculate total
                            if 'price' in item:
                                total += item['quantity'] * item['price']
                            else:
                                items_valid = False
                                errors.append(f"Missing price in order {order['id']}")
                    # Process if items valid
                    if items_valid:
                        # Apply any discounts from settings
                        if settings and 'discount' in settings:
                            total *= (1 - settings['discount'])
                        # Create processed order
                        processed = {
                            'order_id': order['id'],
                            'customer_name': order['customer']['name'],
                            'customer_email': order['customer']['email'],
                            'total': total,
                            'items_count': len(order['items'])
                        }
                        results.append(processed)
                        # Send notification
                        if notify_customer:
                            try:
                                notification = {
                                    'to': order['customer']['email'],
                                    'subject': 'Order Processed',
                                    'total': total
                                }
                                notifications.append(notification)
                                if debug:
                                    print(f"Debug: Notification queued for order {order['id']}")
                            except Exception:
                                errors.append(f"Notification failed for order {order['id']}")
                else:
                    errors.append(f"Invalid customer data in order {order['id']}")
            else:
                errors.append(f"Missing required fields in order {order['id']}")
        except Exception as e:
            errors.append(f"Error processing order {order['id']}: {str(e)}")
            if debug:
                print(f"Debug: Error processing order {order['id']}: {str(e)}")

    if debug:
        print(f"Debug: Processed {len(results)} orders with {len(errors)} errors")
        print(f"Debug: Queued {len(notifications)} notifications")

    return {
        "processed_orders": results,
        "errors": errors,
        "notifications": notifications
}
"""

prompt = f"""I have some code that I'd like you to clean up and improve. Return only the updated code that fixes the issues: {code_snippet}"""
gpt_code = get_chat_completion(GPT_MODEL, prompt)
print(gpt_code)

o1_code = get_chat_completion(O1_MODEL, prompt)
print(o1_code)

result = get_chat_completion(O1_MODEL, f"Which code is better and why? Option 1: {gpt_code}... or Option 2: {o1_code}")
display(Markdown(result))
