from gameFramework.core import *

# G - goal
# Define a simple file management goal
file_management_goal = Goal(
    priority=1,
    name="file_management",
    description="""Manage files in the current directory by:
    1. Listing files when needed
    2. Reading file contents when needed
    3. Searching within files when information is required
    4. Providing helpful explanations about file contents"""
)

def list_files() -> list:
    """List all files in the current directory."""
    return os.listdir('.')

def read_file(file_name: str) -> str:
    """Read and return the contents of a file."""
    with open(file_name, 'r') as f:
        return f.read()

def search_in_file(file_name: str, search_term: str) -> list:
    """Search for a term in a file and return matching lines."""
    results = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i+1, line.strip()))
    return results

# A - actions
# Create and populate the action registry
registry = ActionRegistry()

registry.register(Action(
    name="list_files",
    function=list_files,
    description="List all files in the current directory",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    },
    terminal=False
))

registry.register(Action(
    name="read_file",
    function=read_file,
    description="Read the contents of a specific file",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Name of the file to read"
            }
        },
        "required": ["file_name"]
    },
    terminal=False
))

registry.register(Action(
    name="search_in_file",
    function=search_in_file,
    description="Search for a term in a specific file",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string", 
                "description": "Name of the file to search in"
            },
            "search_term": {
                "type": "string",
                "description": "Term to search for"
            }
        },
        "required": ["file_name", "search_term"]
    },
    terminal=False
))