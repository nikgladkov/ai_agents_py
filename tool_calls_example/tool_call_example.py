from typing import List

from litellm import completion

def parse_response(self, response: str) -> dict:
    raise NotImplementedError("Subclasses must implement this method")

response = completion( 
    model="ollama/llama3.1:latest",
    messages=[{"role": "user", "content": "Get the weather in Belgrade"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather in a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    }],
    tool_choice="auto",
    max_tokens=1024,
    api_base="http://localhost:11434",
    provider="ollama"
)

response_type = type(response)
print(f"\n\nType of response:\n{response_type}")

raw_response = response
print(f"\n\nRaw response:\n{raw_response}")

message = response.choices[0].message
print(f"\n\nMessage:\n{message}")

tool_calls = message.tool_calls
print(f"\n\nTool calls:\n{tool_calls}")

for i, call in enumerate(message.tool_calls, 0):
    print(f"\n\nTool call #{i+1}:\n{call}")
    tool_call = tool_calls[i]
    tool_name = tool_call.function.name
    print(f"\nTool name:\n{tool_name}")