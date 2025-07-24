from typing import Dict, List


class Memory:
    def __init__(self):
        self.items = []  # Basic conversation history

    def add_memory(self, memory: dict):
        """Add memory to working memory"""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> List[Dict]:
        """Get formatted conversation history for prompt"""
        return self.items[:limit]

memory = Memory()

memoryBlock1 = {"field1":"text1", "field2":"text2", "field3":"text3"}
memoryBlock2 = {"field11":"text11","field22":"text22","field33":"text33"}

memory.add_memory(memoryBlock1)

print(memory.get_memories())

memory.add_memory(memoryBlock2)

print(memory.get_memories())