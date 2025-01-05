import io
from PIL import Image
import numpy as np
from app.http_model.response import RouteResponse
from app.http_model.request import RouteRequest
from app.utils.geodata_functions import map_creator
from app.utils.utils import df_factory
from app.model.service import ModelService
from app.optimizer.optimizer import ant_colony_optimization
from app.visualizer.plots import plot_on_map
from loguru import logger
from fastapi import APIRouter


builder_router = APIRouter()

@builder_router.post("/predict")
async def build_route(request: RouteRequest) -> RouteResponse: 

    logger.info(f"Received request to build route for {request.name}")
    df = df_factory(df=request.path)
    ms = ModelService(df, k=request.num_stops)
    
    centers = ms.centers()
    df = ms.df()
    location = (np.mean([center[0] for center in centers]), np.mean([center[1] for center in centers]))
    result = ant_colony_optimization(centers, n_ants=10, n_iterations=1000, alpha=1, beta=1, evaporation_rate=0.5, Q=1)
    logger.info(f"Optimized for best bus route in {request.name}")
    result_map = plot_on_map(df, centers=centers, best_path=result[0], zoom_start=3, location=location)
    logger.info(f"Obtained the map for {request.name}")
    map_creator(input_map=result_map, name=request.name)
    return RouteResponse( 
        name = request.name,
        num_stops = request.num_stops,
        output_path = f"output_folder/{request.name}_bus_map.png"
    )
   