import time
import threading
import random

class AutonomousAgent:
    def __init__(self, name):
        self.name = name
        self.inbox = []
        self.outbox = []
        self.handlers = {}
        self.behaviors = []
        self.running = True

    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)

    def consume_messages(self):
        while self.running:
            if self.inbox:
                message = self.inbox.pop(0)
                self.handle_message(message)
            time.sleep(0.1)  # Sleep to avoid busy waiting

    def handle_message(self, message):
        """Handles a message based on its type or content."""
        message_type = message.get('type')
        handler = self.handlers.get(message_type)

        if not message.get('content'):  # Handle empty message
            print(f"[{self.name}] Received an empty message. Ignoring.")
            return

        if handler:
            handler(message)
        else:
            print(f"[{self.name}] No handler found for message type '{message_type}'")

    def emit_message(self, message):
        """Emits a message to the outbox and checks for duplicates."""
        if message not in self.outbox:
            self.outbox.append(message)
        else:
            print(f"[{self.name}] Duplicate message detected: {message}")

    def run_behaviors(self):
        while self.running:
            for behavior in self.behaviors:
                behavior()
            time.sleep(1)

    def stop(self):
        self.running = False
class ConcreteAgent(AutonomousAgent):
    def __init__(self, name):
        super().__init__(name)
        self.register_handler('filter', self.handle_hello_message)
        self.register_behavior(self.generate_random_message)

    def handle_hello_message(self, message):
        """Prints the message if it contains 'hello'."""
        content = message.get('content')
        if 'hello' in content:
            print(f"[{self.name} Handler]: {content}")

    def generate_random_message(self):
        """Generates a random 2-word message every 2 seconds."""
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = {
            'type': 'filter',
            'content': f"{random.choice(words)} {random.choice(words)}"
        }
        self.emit_message(message)
        time.sleep(2)


if __name__ == "__main__":
    agent1 = ConcreteAgent("Agent1")
    agent2 = ConcreteAgent("Agent2")
    agent1.outbox = agent2.inbox
    agent2.outbox = agent1.inbox
    threading.Thread(target=agent1.consume_messages, daemon=True).start()
    threading.Thread(target=agent1.run_behaviors, daemon=True).start()
    threading.Thread(target=agent2.consume_messages, daemon=True).start()
    threading.Thread(target=agent2.run_behaviors, daemon=True).start()
    time.sleep(10)
    agent1.stop()
    agent2.stop()
