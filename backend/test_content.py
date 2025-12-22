"""
Test script to initialize some content for the chatbot to work with
"""
import asyncio
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.rag.chatbot_service import RAGChatbotService
from src.models.textbook import Textbook

async def setup_test_content():
    """Set up some test content for the chatbot."""
    print("Setting up test content for the chatbot...")

    # Create a test textbook instance
    test_textbook = Textbook(
        id="main-textbook",
        title="AI-Native Textbook for Physical AI & Humanoid Robotics",
        description="Interactive textbook on Physical AI and Humanoid Robotics",
        target_audience="undergraduate",
        content_depth="medium",
        writing_style="academic",
        total_chapters=5,
        generated_content="""
# Chapter 1: Introduction to Physical AI & Humanoid Robotics

Physical AI represents a paradigm shift in artificial intelligence, focusing on systems that interact with the physical world through embodiment, sensing, and actuation. Unlike traditional AI that processes abstract data, Physical AI operates in real environments, requiring integration of perception, reasoning, and action.

## Key Concepts in Physical AI:
- Embodiment: The physical form of AI systems affects their interaction with the world
- Sensorimotor learning: Learning through interaction with physical environments
- Real-time processing: Systems must respond to dynamic physical conditions
- Multi-modal perception: Integration of visual, tactile, auditory, and other sensors

## Humanoid Robotics:
Humanoid robots are designed with human-like characteristics to facilitate natural interaction and compatibility with human environments. They typically feature:
- Bipedal locomotion systems
- Human-like manipulation capabilities
- Social interaction interfaces
- Biomimetic design principles

# Chapter 2: Sensing and Perception

Sensing and perception form the foundation of Physical AI systems. These systems must accurately interpret multi-modal sensory data to understand their environment and make informed decisions.

## Types of Sensors:
- Vision systems (cameras, LIDAR)
- Tactile sensors (force, pressure, temperature)
- Proprioceptive sensors (joint angles, acceleration)
- Auditory systems (microphones for sound processing)

# Chapter 3: Motion and Control

Motion control in Physical AI involves sophisticated algorithms to manage the complex dynamics of physical systems. Control strategies must account for environmental interactions, system dynamics, and real-time constraints.

## Control Approaches:
- Model-based control
- Learning-based control
- Hybrid approaches combining both
- Adaptive control for changing conditions

# Chapter 4: Learning and Adaptation

Physical AI systems must continuously adapt to changing environments and tasks. Learning in physical systems presents unique challenges due to safety requirements, real-time constraints, and the cost of physical interaction.

## Learning Paradigms:
- Reinforcement learning in physical environments
- Imitation learning from human demonstrations
- Transfer learning between simulation and reality
- Continual learning without forgetting previous skills

# Chapter 5: Human-Robot Interaction

Effective human-robot interaction is crucial for Physical AI systems, especially in humanoid robotics. These systems must understand human intentions, communicate effectively, and operate safely in human environments.

## Interaction Modalities:
- Natural language processing
- Gesture recognition
- Emotional intelligence
- Social norm compliance
        """,
        export_formats=["pdf", "epub", "html"],
        metadata={
            "author": "AI Textbook System",
            "created_at": "2024-12-17",
            "version": "1.0"
        }
    )

    # Initialize the chatbot service
    chatbot_service = RAGChatbotService()

    # Index the test textbook
    print("Indexing the test textbook...")
    success = await chatbot_service.index_textbook(test_textbook)

    if success:
        print("SUCCESS: Test textbook indexed successfully!")

        # Test a query to make sure it works
        print("\nTesting a sample query...")
        result = await chatbot_service.query_textbook("main-textbook", "What is Physical AI?")

        print(f"Query result: {result['answer'][:200]}...")
        print("SUCCESS: Chatbot service is working correctly!")

        # Keep the service available for the API
        return chatbot_service
    else:
        print("ERROR: Failed to index the textbook")
        return None

if __name__ == "__main__":
    asyncio.run(setup_test_content())