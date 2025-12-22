"""
Hugging Face Space app for the textbook generation backend
"""
import os
from src.api.main import app

# For Hugging Face Spaces, we need to make sure the app is available at the module level
# The app will be run by the Hugging Face infrastructure
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))