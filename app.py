import eventlet
import logging
import os

eventlet.monkey_patch()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from chat.app import app, run_app  # noqa
from chat.demo_data import create
from chat import utils  # Import utils to access init_redis

if __name__ == "__main__":
    logging.info("Starting application in local development mode")
    
    # Initialize Redis
    utils.init_redis()
    
    # Check if we should create demo data
    if os.environ.get('CREATE_DEMO_DATA', 'True').lower() == 'true':
        logging.info("Creating demo data...")
        create()
    else:
        logging.info("Skipping demo data creation (CREATE_DEMO_DATA is not True)")
    
    # Run the app
    run_app()