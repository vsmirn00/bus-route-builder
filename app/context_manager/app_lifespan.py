from contextlib import asynccontextmanager
from fastapi import FastAPI 
from loguru import logger 

interactive_maps = {}
 
@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info(f"Service ready")

    except Exception as e:
        logger.error(f"Error during lifespan: {e}")
        raise RuntimeError(f"Error during lifespan: {e}")

    yield

    logger.info("Shutting down the application")  
