import eventlet
import logging
import os

eventlet.monkey_patch()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from chat.app import app, run_app  # noqa
from chat import utils

if __name__ == "__main__":
    logging.info("Starting application in local development mode")

    utils.init_redis()

    run_app()
