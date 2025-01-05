from app.model.adapter import ModelAdapter

class ModelService(ModelAdapter):
    
    def __init__(self, dataframe, k=None):
        self.k_means_service = ModelAdapter(dataframe, k)
    
    def centers(self):
        return self.k_means_service.return_centers()

    def df(self):
        return self.k_means_service.return_updated_dataframe()