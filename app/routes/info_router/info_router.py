from fastapi import APIRouter, status
from pydantic import BaseModel

info_router = APIRouter()


class InfoResponse(BaseModel):
    """
    Response model to validate and return when performing an information check.

    Attributes
    ----------
    name : str
        The name of the model.
    version : str
        The version of the model.
    description : str
        A brief description of the model.
    """

    name: str
    version: str
    description: str



@info_router.get(
    "/info",
    tags=["info"],
    summary="Retrieve application information",
    response_description="Return HTTP Status Code 200 (OK) with application information",
    status_code=status.HTTP_200_OK,
    response_model=InfoResponse,
)

def get_info() -> InfoResponse:
    """
    Retrieve information about the application.

    Returns
    -------
    InfoResponse 
        An InfoResponse object containing the model name, version, description.
    """
    return InfoResponse(
        name="Bus line builder",
        version="1.0",
        description="Bus line builder",
    )
