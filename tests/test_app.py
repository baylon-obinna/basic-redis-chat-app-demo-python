import pytest
from chat.app import app  # Adjust the import based on your project structure
from chat import utils
import redis
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_redis_connection(mocker):
    """Test if Redis client is initialized correctly"""
    redis_password = os.getenv('REDIS_PASSWORD', 'default_password')  # Get the password from the environment
    mock_redis = mocker.patch('chat.utils.redis.StrictRedis')
    
    # Call the init_redis function, which should internally use the mocked redis.StrictRedis
    utils.init_redis()
    
    # Assert that redis.StrictRedis was called with the correct arguments
    mock_redis.assert_called_with(host='localhost', port=6379, password=redis_password, db=0)
