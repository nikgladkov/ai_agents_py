import os
import json
from dotenv import load_dotenv
from litellm import completion
from typing import List, Dict

load_dotenv()

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""

    response = completion(
        model="ollama/chevalblanc/gpt-4o-mini:latest",
        messages=messages,
        max_tokens=1024,
        api_base="http://localhost:11434",
        provider="ollama"
    )
    return response.choices[0].message.content

def extract_markdown_block(response: str, keyword: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith(keyword):
        code_block = code_block[6:]

    return code_block

def parse_action(response: str) -> Dict:
	"""Parse the LLM response into a structured action dictionary.""" 
	try: 
		response = extract_markdown_block(response, "action") 
		response_json = json.loads(response) 
		if "tool_name" in response_json and "args" in response_json: 
			return response_json 
		else: 
			return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}} 
	except json.JSONDecodeError: 
		return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}

def list_files() -> str:
    file_list = "file.py, file2.py, file3.py"
	
    return file_list

#Step 1 Constructing the Agent Prompt
messages = [
    {
        "role": "system",
        "content": """ You are an AI agent that can perform tasks by using available tools.

        Available tools: 
        - list_files() -> List[str]: List all files in the current directory.
        - read_file(file_name: str) -> str: Read the content of a file.
        - terminate(message: str): End the agent loop and print a summary to the user.
        
        If a user asks about files, list them before reading. 
        
        Respond always only in English.

        Every response MUST have an action.

        Respond in this format: 
        ```action 
        { 
            "tool_name": "insert tool_name", 
            "args": {...fill in any required arguments here...}
        }
        ```
        """
    }
]

messages.append(
    {
        "role":"user",
        "content": "List all files in the directory with name Test"
    }
)

#Step 2 Generate Response
response = generate_response(messages)

#Step 3 Parse the Response
action = parse_action(response)

#Step 4 Execute the Action
if action["tool_name"] == "list_files":
	result = {"result": list_files()}

#Step 5 Update the Agent’s Memory
messages.append(
    {
        "role":"assistant",
        "content": json.dumps(result)
    })
messages.append(
	{
        "role":"user",
        "content": "Read the content of a file with the name 'file2'"
    })

response = generate_response(messages)
print(response)

#Step 6 Decide Whether to Continue