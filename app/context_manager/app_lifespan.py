from contextlib import asynccontextmanager
from fastapi import FastAPI # type: ignore
from loguru import logger # type: ignore
 
@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info(f"Service ready")

    except Exception as e:
        logger.error(f"Error during lifespan: {e}")
        raise RuntimeError(f"Error during lifespan: {e}")

    yield

    logger.info("Shutting down the application")  
