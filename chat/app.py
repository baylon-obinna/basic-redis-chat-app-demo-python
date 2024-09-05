import os
import sys
import logging

from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO

from chat import utils
from chat.config import get_config
from chat.socketio_signals import io_connect, io_disconnect, io_join_room, io_on_message

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__, static_url_path="", static_folder="../client/build")
app.config.from_object(get_config())
CORS(app)

# Initialize session
sess = Session()
sess.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


# Set up SocketIO event handlers
socketio.on_event("connect", io_connect)
socketio.on_event("disconnect", io_disconnect)
socketio.on_event("room.join", io_join_room)
socketio.on_event("message", io_on_message)

# Import routes
from chat import routes  # noqa

def run_app():
    logging.info("Starting the application...")
    
    # Get port from the command-line arguments or environment variables
    arg = sys.argv[1:]
    port = int(os.environ.get("PORT", 8000))
    if len(arg) > 0:
        try:
            port = int(arg[0])
        except ValueError:
            logging.warning(f"Invalid port argument: {arg[0]}. Using default port {port}.")
    
    logging.info(f"Running the application on port {port}")
    socketio.run(app, port=port, debug=True, use_reloader=True)

application = app

if __name__ == "__main__":
    run_app()