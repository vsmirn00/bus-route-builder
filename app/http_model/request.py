from pydantic import BaseModel

class RouteRequest(BaseModel):
    name: str
    num_stops: int
    path: str

    model_config = {
        "request": {
            "name": "Viladecans",
            "num_stops": 13,
            "path": "data/russia_cities.geojson"
        }
    }
