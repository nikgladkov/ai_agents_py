import os
import json
from dotenv import load_dotenv
from litellm import completion
from typing import List, Dict

load_dotenv()

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""

    response = completion(
        model="ollama/magicoder:7b",
        messages=messages,
        max_tokens=1024,
        api_base="http://localhost:11434"
    )

    return response.choices[0].message.content

code_spec = {
    'name': 'UI Test for the main page',
    'description': 'Main page has one input field and submit button under it. Click button submits the text from the input field. If there is no text typed button is unclickable.',
    'params': {
        'button css selector': '.button',
        'input css selector': '.input'
    },
}

messages = [
    {"role": "system", "content": "Act as a QA automation expert proficient in Cypress and TypeScript. When asked to write test scripts, follow best practices for maintainability, readability, and reusability."},
    {"role": "user", "content": f"Please write the UI test based on the code specification: {json.dumps(code_spec)}"}
]

response = generate_response(messages)
print(response)

messages = [
    {"role": "system", "content": "Act as a QA automation expert proficient in Cypress and TypeScript. When asked to write test scripts, follow best practices for maintainability, readability, and reusability."},
    {"role": "assistant", "content": response},
    {"role": "user", "content": "Add alert with text ""Test"" in the end of the test case"}
]

response = generate_response(messages)
print(response)