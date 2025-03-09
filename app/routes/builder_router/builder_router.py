import numpy as np
from app.http_model.response import RouteResponse
from app.http_model.request import RouteRequest
from app.utils.utils import map_creator
from app.model.service import ModelService
from loguru import logger
from fastapi import APIRouter
from app.context_manager.app_lifespan import interactive_maps

builder_router = APIRouter()

@builder_router.post("/predict")
async def build_route(request: RouteRequest) -> RouteResponse: 

    logger.info(f"Received request to build route for {request.name}")
    model = ModelService()
    logger.info(f"Preparing file {request.input_path}")
    response, maps = model.predict(request)

    logger.info(f"Obtained the map for {request.name}")
    map_creator(input_map=maps, request=request)
    interactive_maps["map"] = maps
    return response
   