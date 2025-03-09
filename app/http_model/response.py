from typing import List, Optional
from pydantic import BaseModel

class RouteResponse(BaseModel):
    name: str
    input_path: str
    output_path: str
    num_stations: Optional[int] = None 
    num_routes: Optional[int] = None 
    central_station: Optional[bool] = None 
    balanced_num_stops: Optional[bool] = None 
    results: List

    model_config = {
        "response": {
            "name": "Viladecans",
            "input_path": "data/equipaments_model.csv",
            "output_path": "output_folder/image.jpg",
            "num_stations": 30,
            "num_routes": 3,
            "central_station": True,
            "balanced_num_stops": True,
            "results": [{"route_id": 2,
           "route_num_stations": 3,
           "distance": 10.23
           }]
        }
    }

class MapResponse(BaseModel):

    route_id: int
    route_num_stations: int
    distance: float

    model_config = {"route_id": 2,
           "route_num_stations": 3,
           "distance": 10.23
           }