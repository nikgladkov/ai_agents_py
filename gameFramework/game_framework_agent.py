# Adapted from an example provided in a Coursera course - AI Agents and Agentic AI with Python & Generative AI
# Original code: https://colab.research.google.com/drive/1FezaORGZ4qSznCEZRQOwUUiiSeYCDa5z?usp=sharing#scrollTo=6PC3ncxezoJC

import json
import os
from typing import List
from litellm import completion
from gameFramework.core import Prompt, Goal, Action, ActionRegistry, Memory, Environment, AgentFunctionCallingActionLanguage, Agent 

def generate_response(prompt: Prompt) -> str:
    """Call LLM to get response"""

    messages = prompt.messages
    tools = prompt.tools

    result = None

    if not tools:
        response = completion(
            model="ollama/llama3.1:latest",
            messages=messages,
            max_tokens=1024,
            api_base="http://localhost:11434",
            provider="ollama"
        )
        result = response.choices[0].message.content
    else:
        response = completion(
            model="ollama/llama3.1:latest",
            messages=messages,
            tools=tools,
            max_tokens=1024,
            api_base="http://localhost:11434",
            provider="ollama"
        )

        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            result = json.dumps(result)
        else:
            result = response.choices[0].message.content

    return result

# Define the agent's goals
goals = [
    Goal(priority=1, name="Gather Information", description="Read each file in the project"),
    Goal(priority=1, name="Terminate", description="Call the terminate call when you have read all the files and provide the content of the README in the terminate message")
    ]

# Define the agent's language
agent_language = AgentFunctionCallingActionLanguage()

def read_project_file(name: str) -> str:
    with open(name, "r") as f:
        return f.read()

def list_project_files() -> List[str]:
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])

# Define the action registry and register some actions
action_registry = ActionRegistry()
 
action_registry.register(Action(
    name="list_project_files",
    function=list_project_files,
    description="Lists all files in the project.",
    parameters={},
    terminal=False
))

action_registry.register(Action(
    name="read_project_file",
    function=read_project_file,
    description="Reads a file from the project.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    },
    terminal=False
))

action_registry.register(Action(
    name="terminate",
    function=lambda message: f"{message}\nTerminating...",
    description="Terminates the session and prints the message to the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": []
    },
    terminal=True
))

# Define the environment
environment = Environment()

# Create an agent instance
agent = Agent(goals, agent_language, action_registry, generate_response, environment)

# Run the agent with user input
user_input = "How many files are in the directory?"
final_memory = agent.run(user_input)

# Print the final memory
print(final_memory.get_memories())