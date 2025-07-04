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

def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]

    return code_block

# First Prompt:
# Ask the user what function they want to create
# Ask the LLM to write a basic Python function based on the user’s description
# Store the response for use in subsequent prompts
# Parse the response to separate the code from the commentary by the LLM

print("\nWhat function you want to create? Please describe")
print("Your description: ", end='')
function_description = input().strip()

messages = [
    {
        "role": "system", 
        "content": "You are python developer"
    }
]

messages.append({
        "role": "user", 
        "content": f"Write a basic Python function based on the user's description: {function_description}. Output the function in a ```python code block```."
    })

response = generate_response(messages)
function_code = extract_code_block(response)

print(f"\n\n----------------\n\n")
print(f"1. The code snippet:\n{function_code}")

# Second Prompt:
# Pass the code generated from the first prompt
# Ask the LLM to add comprehensive documentation including:
# Function description
# Parameter descriptions
# Return value description
# Example usage
# Edge cases

messages.append({
    "role": "assistant",  
    "content": function_code
})

messages.append({
    "role": "user",
    "content": "Add documentation to this function according to the list: 1.Function description; 2.Parameter descriptions; 3. Return value description; 4.Example usage; 5.Edge cases;"
})

response = generate_response(messages)
function_code_description = response

print(f"\n\n----------------\n\n")
print(f"2. Description:\n{function_code_description}")

# Third Prompt:

# Pass the documented code generated from the second prompt
# Ask the LLM to add test cases using Python’s unittest framework
# Tests should cover:
# Basic functionality
# Edge cases
# Error cases
# Various input scenarios

messages.append({
    "role": "assistant",  
    "content": function_code_description
})

messages.append({
    "role": "user",
    "content": "add test cases using Python’s unittest framework. Tests should cover: Basic functionality, Edge cases, Error cases, Various input scenarios. Output the code of tests in a ```python code block```."
})

response = generate_response(messages)
function_unit_tests = extract_code_block(response)

print(f"\n\n----------------\n\n")
print(f"3. Unit tests:\n{function_unit_tests}")

print(f"\n\n----------------\n\n")