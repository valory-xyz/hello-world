import unittest
from autonomous_agent import AutonomousAgent, ConcreteAgent
import time


class TestAutonomousAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up two agents for testing."""
        self.agent1 = ConcreteAgent("TestAgent1")
        self.agent2 = ConcreteAgent("TestAgent2")
        self.agent1.outbox = self.agent2.inbox
        self.agent2.outbox = self.agent1.inbox

    def tearDown(self):
        """Stop agents after each test."""
        self.agent1.stop()
        self.agent2.stop()

    def test_handler_registration(self):
        """Test if handlers are registered correctly."""
        self.assertIn('filter', self.agent1.handlers)
        self.assertIsNotNone(self.agent1.handlers['filter'])

    def test_behavior_registration(self):
        """Test if behaviors are registered correctly."""
        self.assertEqual(len(self.agent1.behaviors), 1)
        self.assertEqual(len(self.agent2.behaviors), 1)

    def test_empty_message_handling(self):
        """Test how the agent handles empty messages."""
        self.agent1.inbox.append({'type': 'filter', 'content': ''})
        self.agent1.handle_message(self.agent1.inbox[0])

    def test_duplicate_message_detection(self):
        """Test if the agent detects duplicate messages."""
        message = {'type': 'filter', 'content': 'hello world'}
        self.agent1.emit_message(message)
        self.agent1.emit_message(message)  
        self.assertEqual(len(self.agent1.outbox), 1, "Duplicate message was added.")

    def test_message_passing_between_agents(self):
        """Test message passing between two agents."""
        message = {'type': 'filter', 'content': 'hello moon'}
        self.agent1.emit_message(message)
        time.sleep(0.2)  # Wait a little for message processing
        self.assertIn(message, self.agent2.inbox)

    def test_unhandled_message_type(self):
        """Test handling of unhandled message types."""
        message = {'type': 'unknown', 'content': 'test message'}
        self.agent1.emit_message(message)
        self.agent1.handle_message(message)
        # Expect it to print a warning about unhandled message types (visually confirmed)

    def test_behavior_generates_messages(self):
        """Test if behaviors generate messages correctly."""
        initial_length = len(self.agent1.outbox)
        self.agent1.generate_random_message()
        self.assertEqual(len(self.agent1.outbox), initial_length + 1)

    def test_stop_agent(self):
        """Test if the agent stops correctly."""
        self.agent1.stop()
        self.assertFalse(self.agent1.running, "Agent did not stop correctly.")

    def test_communication_integration(self):
        """Integration test for two agents communicating."""
        self.agent1.emit_message({'type': 'filter', 'content': 'hello space'})
        time.sleep(0.5)
        self.assertTrue(any('hello' in msg['content'] for msg in self.agent2.inbox),
                        "Integration between agents failed.")


if __name__ == '__main__':
    unittest.main()
