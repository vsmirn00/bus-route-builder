from app.model.adapter import ModelAdapter

class ModelService(ModelAdapter):
    """
    Service class for handling model predictions using ModelAdapter.
    """
    
    def __init__(self):
        """
        Initializes the ModelService class.
        """
        self.bus_router_service = ModelAdapter()

    def predict(self, request):
        """
        Runs the prediction process using the bus routing service.

        Parameters
        ----------
        request : object
            The request object containing input data for prediction.

        Returns
        -------
        tuple
            - dict: Parsed output containing optimized routes and metadata.
            - folium.Map: A merged Folium map displaying the optimized routes.
        """
        return self.bus_router_service.predict(request)
