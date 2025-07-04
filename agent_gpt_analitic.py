from typing import List, Dict
from litellm import completion

def generate_response_analitic(messages: List[Dict]) -> str:
    response = completion(
        model="ollama/chevalblanc/gpt-4o-mini:latest",
        messages=messages,
        max_tokens=1024,
        api_base="http://localhost:11434",
        provider="ollama"
    )
    return response.choices[0].message.content

messages = [
    {
        "role": "system",
        "content": """
            You are a senior analyst with a deep understanding hot to create tasks for python developers.

            You will follow the rules:
             - Respond always only in English
             - Start each answer with "QA Analysis:" and then provide a clear, structured answer
             - always wrap the code in ``` ```
        """
    }
]

messages.append(    {
        "role": "user", 
        "content": "I need code specification for the python - should be a script that prints Hello world 10 times and stops."
    })

print(generate_response_analitic(messages))