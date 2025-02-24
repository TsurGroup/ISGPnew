import multiprocessing
import os
import sys
import threading
import webbrowser
import uvicorn
import logging
from main import app  # Import your FastAPI app from the 'main' module

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Determine the port from the environment variable or default to 8000
port = int(os.getenv('PORT', 8000))

def open_browser():
    # Wait for a short time to ensure the server is ready
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    logging.info('Starting the FastAPI app')
    try:
        # Run the FastAPI app
        if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
          multiprocessing.freeze_support()
        threading.Timer(1.5, open_browser).start()

        uvicorn.run(app, host="0.0.0.0", port=port)
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
