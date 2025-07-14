from litellm import completion
import json
import sys

# Using LLM Function Calling for Structured Execution

# 1.Define the Tool Functions
def double_number(number: int) -> int:
    return int(number)*2

def triple_number(number: int) -> int:
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
            "description": "Returns the result of doubling the input integer",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer"},
                },
                "required": ["number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "triple_number",
            "description": "Returns the result of tripling the input integer",
             "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer"},
                },
                "required": ["number"]
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

print(f"\n-------------")
print(f"\ntool: {tool}")

#gets function name value
try:
    #tool_name = tool.function.name
    tool_name = tool.get("function", {}).get("name")
except Exception as e:
    print(f"\nCouldn't determine the tool for the user task \"{user_task}\" : {e}")
    sys.exit()

print(f"\ntool_name: {tool_name}")

#parses function arguments
try:
    #tool_args = json.loads(tool.function.arguments)
    tool_args = json.loads(tool.get("function", {}).get("arguments", "{}"))
except Exception as e:
    print(f"\nCouldn't determine the tool for the user task \"{user_task}\" : {e}")
    sys.exit()

print(f"\ntool_args: {tool_args}")

# 8. Execute the Function with the Provided Arguments
result = tool_functions[tool_name](**tool_args)

print(f"\n-------------")
print(f"\nuser_task: {user_task}")
print(f"\nresult: {result}")