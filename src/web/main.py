from fastapi import FastAPI, Request, Header
from starlette.responses import JSONResponse
from src.web.auth import AuthrizeRequestMiddleware
from src.jwt_generator import generate_jwt

app = FastAPI()
app.add_middleware(middleware_class=AuthrizeRequestMiddleware)

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "This is a public endpoint"})

@app.get("/fake")
def read_fake(request: Request, authorization: str = Header(None)):
    user_id = request.state.user_id
    return JSONResponse(content={"message": f"This is a required authentication endpoint. Your user ID is: {user_id}"})

@app.get("/token")
def generate_token():
    jwt_token = generate_jwt()
    return JSONResponse(content={"message": "JWT token generated", "token": jwt_token})