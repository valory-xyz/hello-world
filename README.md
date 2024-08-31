Autonomous Agent System
This project implements a basic autonomous agent framework with reactive and proactive behavior capabilities. The agents can handle incoming messages, generate behaviors, and interact with each other in a simulated environment.

Overview
The system consists of two main components:

AutonomousAgent Class: A base class that provides the core functionalities for handling messages, registering handlers, and executing behaviors.

ConcreteAgent Class: A subclass of AutonomousAgent that implements specific behaviors and message handling logic. This agent generates random messages and handles those containing the word "hello."

Features
Message Handling: Agents can receive messages and process them based on registered handlers.
Behavior Execution: Agents can perform proactive behaviors at defined intervals.
Duplicate Message Detection: Ensures that duplicate messages are not processed multiple times.
Concurrent Execution: Agents run their message-handling and behavior-execution loops concurrently using threads.
Graceful Shutdown: Agents can be stopped cleanly, halting all operations.
How It Works
Agent Initialization: Each agent is created with a unique name and can register handlers and behaviors.
Message Handling: Messages are consumed from the inbox and processed by the corresponding handler if registered.
Behavior Execution: Behaviors are executed in a loop, generating messages or performing other actions.
Communication: Agents communicate by emitting messages into each other’s inboxes, allowing for dynamic interaction.
