"""
Script to set up content for the chatbot by creating a textbook and indexing it via the API
"""
import requests
import time
import json

def setup_textbook_and_index():
    """Create a textbook and index it for the chatbot."""
    base_url = "http://localhost:8000"

    print("Creating a textbook for the chatbot...")

    # Step 1: Create a textbook
    generation_params = {
        "id": "params_" + str(int(time.time())),
        "topic": "AI-Native Textbook for Physical AI & Humanoid Robotics",
        "target_audience": "undergraduate",
        "num_chapters": 5,
        "content_depth": "medium",
        "writing_style": "academic",
        "sections_per_chapter": 4,
        "include_examples": True,
        "include_exercises": True,
        "required_sources": ["Physical AI", "Humanoid Robotics"],
        "excluded_topics": [],
        "custom_instructions": "Focus on interactive and engaging content for students"
    }

    try:
        # Create the textbook
        response = requests.post(f"{base_url}/api/textbook-generation/generate", json=generation_params)

        if response.status_code == 200:
            result = response.json()
            textbook_id = result.get("textbook_id")
            print(f"SUCCESS: Textbook creation started with ID: {textbook_id}")

            # Wait for generation to complete
            print("Waiting for textbook generation to complete...")
            status_url = f"{base_url}/api/textbook-generation/status/{textbook_id}"

            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                status_response = requests.get(status_url)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"  Progress: {status_data['progress']:.1%} - {status_data['message']}")

                    if status_data['status'] == 'completed':
                        print("SUCCESS: Textbook generation completed!")
                        break
                    elif status_data['status'] == 'failed':
                        print("ERROR: Textbook generation failed!")
                        return False
            else:
                print("WARNING: Generation may still be in progress, continuing...")

            # Step 2: Index the textbook for RAG
            print(f"Indexing textbook {textbook_id} for RAG...")
            index_response = requests.post(f"{base_url}/api/rag/index", params={"textbook_id": textbook_id})

            if index_response.status_code == 200:
                index_result = index_response.json()
                print(f"SUCCESS: {index_result['message']}")

                # Step 3: Verify the textbook is indexed
                info_response = requests.get(f"{base_url}/api/rag/info/{textbook_id}")
                if info_response.status_code == 200:
                    info = info_response.json()
                    print(f"SUCCESS: Textbook info available: {info['title']}")
                    print("SUCCESS: Chatbot content setup completed successfully!")
                    print(f"SUCCESS: You can now ask questions about textbook ID: {textbook_id}")
                    return True
                else:
                    print(f"ERROR: Could not verify textbook info: {info_response.status_code}")
                    return True  # Still return True as indexing succeeded
            else:
                print(f"ERROR: Failed to index textbook: {index_response.status_code} - {index_response.text}")
                return False

        else:
            print(f"ERROR: Failed to create textbook: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the backend server. Please make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"ERROR: Error setting up textbook: {str(e)}")
        return False

if __name__ == "__main__":
    print("Setting up content for the chatbot...")
    success = setup_textbook_and_index()

    if success:
        print("\n" + "="*60)
        print("SUCCESS: Chatbot content has been set up!")
        print("Your chatbot should now be able to answer questions about:")
        print("- Physical AI")
        print("- Humanoid Robotics")
        print("- Textbook content and concepts")
        print("\nTry asking questions like:")
        print("- 'What is Physical AI?'")
        print("- 'Tell me about chapter 1'")
        print("- 'Explain humanoid robotics'")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("FAILED: Chatbot content setup failed!")
        print("Please make sure:")
        print("1. The backend server is running on http://localhost:8000")
        print("2. All dependencies are properly installed")
        print("="*60)