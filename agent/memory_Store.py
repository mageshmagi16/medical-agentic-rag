from collections import defaultdict
from typing import List, Dict

class MemoryStore:
    def __init__(self):
        self.store = defaultdict(list)

    def get(self, chat_id: str) -> List[Dict]:
        return self.store[chat_id]

    def add(self, chat_id: str, role: str, content: str):
        self.store[chat_id].append({
            "role": role,
            "content": content
        })

    def last_n(self, chat_id: str, n: int = 6):
        return self.store[chat_id][-n:]