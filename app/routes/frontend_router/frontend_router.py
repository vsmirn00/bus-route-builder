from fastapi import APIRouter
from app.context_manager.app_lifespan import interactive_maps
from fastapi.responses import HTMLResponse, JSONResponse

frontend_router = APIRouter()

@frontend_router.get("/map", response_class=HTMLResponse)
def get_map():
    if interactive_maps["map"] is not None:
        return interactive_maps["map"]._repr_html_()
    else:
        return JSONResponse(content={"error": "No map available. Generate a map first."}, status_code=404)
