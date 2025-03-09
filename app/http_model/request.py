from typing import Optional
from pydantic import BaseModel

class RouteRequest(BaseModel):
    name: str
    input_path: str
    output_path: Optional[str] = "output_folder/" 
    num_stations: Optional[int] = 0 
    num_routes: Optional[int] = 0 
    central_station: bool
    balance_stations: bool

    model_config = {
        "response": {
            "name": "Viladecans",
            "input_path": "data/equipaments_model.csv",
            "output_path": "output_folder/",
            "num_stations": 0,
            "num_routes": 0,
            "central_station": True,
            "balance_stations": True
        }
    }



