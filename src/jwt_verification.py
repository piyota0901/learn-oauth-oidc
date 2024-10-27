from pathlib import Path

# 公開鍵RS256アルゴリズムでJWTを検証する
import jwt
from cryptography.hazmat.primitives import serialization

def verify_jwt(jwt_token: str) -> dict:
    """JWTトークンを検証する

    Args:
        jwt_token (str): JWTトークン

    Returns:
        dict: _description_
    """
    public_key_text = (Path(__file__).parent.parent / Path("pubkey.pem")).read_text()
    public_key = serialization.load_pem_public_key(data=public_key_text.encode())
    
    try:
        payload = jwt.decode(
                        jwt=jwt_token, 
                        key=public_key, 
                        algorithms=["RS256"], 
                        audience="my_audience"
                    )
    
    except jwt.ExpiredSignatureError:
        raise Exception("JWTトークンの有効期限が切れています")
    
    return payload

if __name__ == "__main__":
    jwt_token = input("Please enter the JWT token: ")
    print(verify_jwt(jwt_token))