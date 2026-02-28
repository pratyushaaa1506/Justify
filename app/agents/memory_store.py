from collections import defaultdict, deque
from typing import List, Dict

class MemoryStore:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.sessions = defaultdict(lambda: deque(maxlen=self.max_messages))

    def add_message(self, session_id: str, role: str, content: str):
        self.sessions[session_id].append({"role": role, "content": content})

    def get_memory(self, session_id: str) -> List[Dict[str, str]]:
        return list(self.sessions[session_id])

    def clear(self, session_id: str):
        self.sessions[session_id].clear()
