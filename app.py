from chat.app import app, run_app  # noqa
from chat.demo_data import create  


if __name__ == "__main__":
    # monkey patch is "required to force the message queue package to use coroutine friendly functions and classes"
    # check flask-socketio docs https://flask-socketio.readthedocs.io/en/latest/
    import eventlet

    eventlet.monkey_patch()
    create()
    run_app()
