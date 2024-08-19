import os

import redis
from werkzeug.utils import import_string


class Config(object):
    REDIS_URL = os.environ.get("REDIS_URL", "redis://:redispass@redis:6379/0")
    SECRET_KEY = os.environ.get("SECRET_KEY", "Optional default value")
    SESSION_TYPE = "redis"
    redis_client = redis.Redis.from_url(REDIS_URL)
    SESSION_REDIS = redis_client


class ConfigDev(Config):
    # DEBUG = True
    pass


class ConfigProd(Config):
    pass


def get_config() -> Config:
    return import_string(os.environ.get("CHAT_CONFIG", "chat.config.ConfigDev"))
