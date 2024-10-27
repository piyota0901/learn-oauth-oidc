from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization

def generate_jwt():
    now = datetime.now(timezone.utc)
    payload = {
        "iss": "https://auth.myapp.io/",
        "sub": "b567dd8f-6bb5-4d2c-b66f-b1816b5d4dc1", # python -c "import uuid;print(uuid.uuid4())",
        "aud": "my_audience",
        "iat": now.timestamp(),
        "exp": (now + timedelta(minutes=5)).timestamp(),
        "scope": "openid",
    }
    
    private_key_text = (Path(__file__).parent.parent  / Path("private_key.pem")).read_text()
    private_key = serialization.load_pem_private_key(data=private_key_text.encode(),password=None)
    
    return jwt.encode(payload=payload, key=private_key, algorithm="RS256")

if __name__ == "__main__":
    print(generate_jwt())