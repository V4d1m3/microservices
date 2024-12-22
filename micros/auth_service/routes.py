import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import schemas, utils, jwt_handler

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])

DATABASE_SERVICE_URL = "http://db_service:8090"

@router.post("/register", response_model=schemas.UserOut)
async def register(user: Annotated[schemas.UserCreate, Depends()]):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    logger.info(f"Registering user: {user.username}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATABASE_SERVICE_URL}/users/",
            json={
                "username": user.username,
                "hashed_password": utils.hash_password(user.password)
            }
        )
        if response.status_code != 200:
            logger.error(f"Failed to register user: {response.json()}")
            raise HTTPException(status_code=response.status_code, detail=response.json())
        logger.info(f"User registered successfully: {user.username}")
        return response.json()

@router.post("/login", response_model=schemas.Token)
async def login(user: Annotated[schemas.UserCreate, Depends()]):
    """
    Эндпоинт для входа пользователя в систему.
    """
    logger.info(f"User login attempt: {user.username}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DATABASE_SERVICE_URL}/users/by-username/?username={user.username}")
            if response.status_code == 404:
                logger.warning(f"User not found: {user.username}")
                raise HTTPException(status_code=401, detail="Invalid credentials")
            response.raise_for_status()  # Проверяем на другие коды ошибок
            db_user = response.json()

            if "hashed_password" not in db_user:
                logger.error(f"Missing 'hashed_password' in response for user: {user.username}")
                raise HTTPException(status_code=500, detail="Unexpected database response")

            if not utils.verify_password(user.password, db_user["hashed_password"]):
                logger.warning(f"Invalid password for user: {user.username}")
                raise HTTPException(status_code=401, detail="Invalid credentials")

            access_token = jwt_handler.create_access_token({"sub": str(db_user["id"])})
            logger.info(f"User logged in successfully: {user.username}")
            return {"access_token": access_token, "token_type": "bearer"}
    except httpx.RequestError as e:
        logger.error(f"Error during request to database service: {str(e)}")
        raise HTTPException(status_code=500, detail="Database service unavailable")
    #except Exception as e:
        #logger.error(f"Unexpected error: {str(e)}")
        #raise HTTPException(status_code=500, detail="Internal server error")


security = HTTPBearer()

@router.post("/verify-token")
def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Эндпоинт для проверки токена пользователя.
    """
    logger.info("Verifying token")
    payload = jwt_handler.decode_access_token(token.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        logger.error("Invalid token payload")
        raise HTTPException(status_code=401, detail="Invalid token payload")
    logger.info(f"Token verified successfully for user_id: {user_id}")
    return {"user_id": int(user_id)}
