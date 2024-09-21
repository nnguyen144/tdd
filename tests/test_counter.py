"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest

# we need to import the unit under test - counter
from src.counter import app, create_counter

# we need to import the file that contains the status codes
from src import status

@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        """It should update a counter"""
        result = client.post('/counters/swag')
        assert result.status_code == status.HTTP_201_CREATED
        num = client.get('/counters/swag')
        assert num.status_code == status.HTTP_200_OK
        result = client.put('/counters/swag')
        assert result.status_code == status.HTTP_200_OK
        result = client.get('/counters/swag')
        assert result.status_code == status.HTTP_200_OK
        assert result.get_json()["swag"] == num.get_json()["swag"] + 1

    def test_update_a_counter_fail(self, client):
        result = client.put('/counters/swag3')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_read_a_counter(self, client):
        """It should read a counter"""
        result = client.post('/counters/swag2')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.get('/counters/swag2')
        assert result.status_code == status.HTTP_200_OK
        assert result.get_json()["swag2"] == 0

    def test_read_a_counter_fail(self, client):
        result = client.get('/counters/swag4')
        assert result.status_code == status.HTTP_404_NOT_FOUND