from pydantic import BaseModel

class RouteResponse(BaseModel):
    name: str
    num_stops: int
    output_path: str

    model_config = {
        "response": {
            "name": "Viladecans",
            "num_stops": 13,
            "output_path": "output_folder/image.jpg"
        }
    }
