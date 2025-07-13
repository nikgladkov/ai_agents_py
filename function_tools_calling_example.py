from litellm import completion
import json
import sys

# Using LLM Function Calling for Structured Execution

# 1.Define the Tool Functions
def double_number(number):
    return int(number)*2

def triple_number(number):
    return int(number)*3

# 2.Create a Function Registry
tool_functions = {
    "double_number": double_number,
	"triple_number": triple_number
	}

# 3.Define Tool Specifications Using JSON Schema**
tools = [
    {
        "type": "function",
        "function": {
            "name": "double_number",
            "description": "Doubles the input integer",
            "parameters": {
                "type": "integer only",
                "required": "yes"
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "triple_number",
            "description": "Triples the input integer",
            "parameters": {
                "type": "integer only",
                "required": "yes"
            }
        }
    }
]

# 4.Set Up the Agent’s Instructions
agent_rules = [{
    "role":"system",
    "content":"""
    You are an AI agent that can perform tasks by using available tools."""
}]

# 5. Prepare the Conversation Context
user_task = input("\nDouble or Triple? What's the number?\n")
memory = [{"role": "user", "content": user_task}]
messages = agent_rules + memory

# 6. Make the API Call with Function Definitions
response = completion( 
	model="ollama/chevalblanc/gpt-4o-mini:latest", 
	messages=messages, 
	tools=tools, 
	max_tokens=1024,
    api_base="http://localhost:11434",
    provider="ollama"
)

# 7. Process the Structured Response

#gets first element from the tool_calls
try:
    tool = response.choices[0].message.tool_calls[0]
except Exception as e:
    print(f"\nCouldn't determine the tool for the user task \"{user_task}\" : {e}")
    sys.exit()

#gets function name value
try:
    tool_name = tool.function.name
except Exception as e:
    print(f"\nCouldn't determine the tool for the user task \"{user_task}\" : {e}")
    sys.exit()

#parses function arguments
try:
    tool_args = json.loads(tool.function.arguments)
except Exception as e:
    print(f"\nCouldn't determine the tool for the user task \"{user_task}\" : {e}")
    sys.exit()

# 8. Execute the Function with the Provided Arguments

result = tool_functions[tool_name](**tool_args)

print(f"\n-------------")
print(f"\ntool: {tool}")
print(f"\ntool_name: {tool_name}")
print(f"\ntool_args: {tool_args}")
print(f"\n-------------")
print(f"\nuser_task: {user_task}")
print(f"\nresult: {result}")