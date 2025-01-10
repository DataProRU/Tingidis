import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from web_app.main import app
from web_app.services.auth_service import create_token

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@pytest.fixture
async def authorized_api_client(sample_user):
    transport = ASGITransport(app=app)

    # Use the AsyncClient with the transport
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Generate JWT token for the user
        token = create_token(
            data={"sub": sample_user.username, "role": sample_user.role},
            key=SECRET_KEY,
            algoritm=ALGORITHM,
        )

        # Add the token to client headers
        client.headers = {
            "Authorization": f"Bearer {token}"
        }

        yield client



@pytest.fixture
def unauthorized_api_client():
    client = TestClient(app)
    yield client