import json
import math
import random
import logging
import os
import redis

import bcrypt

from chat import demo_data
from chat.config import Config

SERVER_ID = random.uniform(0, 322321)

redis_client = Config.redis_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def make_username_key(username):
    return f"username:{username}"


def create_user(username, password):
    logging.info(f"Creating user: {username}")
    username_key = make_username_key(username)
    # Create a user
    hashed_password = bcrypt.hashpw(str(password).encode("utf-8"), bcrypt.gensalt(10))
    next_id = redis_client.incr("total_users")
    user_key = f"user:{next_id}"
    redis_client.set(username_key, user_key)
    redis_client.hmset(user_key, {"username": username, "password": hashed_password})

    redis_client.sadd(f"user:{next_id}:rooms", "0")
    logging.info(f"User created with ID: {next_id}")

    return {"id": next_id, "username": username}


def get_messages(room_id=0, offset=0, size=50):
    """Check if room with id exists; fetch messages limited by size"""
    room_key = f"room:{room_id}"
    room_exists = redis_client.exists(room_key)
    if not room_exists:
        return []
    else:
        values = redis_client.zrevrange(room_key, offset, offset + size)
        return list(map(lambda x: json.loads(x.decode("utf-8")), values))


def hmget(key, key2):
    """Wrapper around hmget to unpack bytes from hmget"""
    result = redis_client.hmget(key, key2)
    return list(map(lambda x: x.decode("utf-8"), result))


def get_private_room_id(user1, user2):
    if math.isnan(user1) or math.isnan(user2) or user1 == user2:
        return None
    min_user_id = user2 if user1 > user2 else user1
    max_user_id = user1 if user1 > user2 else user2
    return f"{min_user_id}:{max_user_id}"


def create_private_room(user1, user2):
    logging.info(f"Creating private room for users {user1} and {user2}")
    """Create a private room and add users to it"""
    room_id = get_private_room_id(user1, user2)
    if not room_id:
        return None, True

    # Add rooms to those users
    redis_client.sadd(f"user:{user1}:rooms", room_id)
    redis_client.sadd(f"user:{user2}:rooms", room_id)
    logging.info(f"Private room created with ID: {room_id}")

    return (
        {
            "id": room_id,
            "names": [
                hmget(f"user:{user1}", "username"),
                hmget(f"user:{user2}", "username"),
            ],
        },
        False,
    )


def init_redis():
    if getattr(init_redis, 'initialized', False):
        logging.info("Redis already initialized, skipping.")
        return

    logging.info("Initializing Redis...")
    total_users_exist = redis_client.exists("total_users")
    if not total_users_exist:
        logging.info("Setting up initial Redis data...")
        redis_client.set("total_users", 0)
        redis_client.set(f"room:0:name", "General")
    
    if os.environ.get('CREATE_DEMO_DATA', 'True').lower() == 'true':
        if not total_users_exist:
            logging.info("Creating demo data...")
            from chat.demo_data import create
            create()
        else:
            logging.info("Demo data already exists, skipping creation.")
    else:
        logging.info("Demo data creation skipped (CREATE_DEMO_DATA is not True).")
    
    logging.info("Redis initialization complete.")
    init_redis.initialized = True
# We use event stream for pub sub. A client connects to the stream endpoint and listens for the messages

def event_stream():
    """Handle message formatting, etc."""
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("MESSAGES")
    for message in pubsub.listen():
        message_parsed = json.loads(message["data"])
        if message_parsed["serverId"] == SERVER_ID:
            continue

        data = "data:  %s\n\n" % json.dumps(
            {"type": message_parsed["type"], "data": message_parsed["data"],}
        )
        yield data