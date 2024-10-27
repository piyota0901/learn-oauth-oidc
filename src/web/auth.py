from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError
)

from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


public_key_text = (Path(__file__).parent.parent.parent / Path("public_key.pem")).read_text()
public_key = load_pem_x509_certificate(data=public_key_text.encode()).public_key()

def decode_and_verify_token(token: str) -> dict:
    """アクセストークンをデコードして検証する

    Args:
        token (str): _description_

    Returns:
        dict: _description_
    """
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=["RS256"],
        audience="my_audience"
    )

class AuthrizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, 
        request: Request, 
        call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in ["/", "/docs", "/openapi.json", "/token"]:
            return await call_next(request) # ルートパスとドキュメントパスは認証をスキップ
        
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Access token must be provided in the Authorization header"
                }
            )
        
        try:
            auth_token = bearer_token.split(" ")[1] # Authorization: Bearer <token> -> <token>
            token_payload = decode_and_verify_token(token=auth_token)
        except (
            InvalidTokenError,
            InvalidAlgorithmError,
            ImmatureSignatureError,
            ExpiredSignatureError,
            InvalidAudienceError,
            MissingRequiredClaimError,
            InvalidKeyError,
            InvalidSignatureError
        ) as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid access token",
                    "body": str(e)
                }
            )
        else:
            request.state.user_id = token_payload["sub"]
        
        return await call_next(request)