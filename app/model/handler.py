from sklearn.cluster import KMeans
from app.model.abstract_base_class import AbstractBaseClass

class ModelHandler(AbstractBaseClass):
    def __init__(self):
        self.model = None
        self.k = 3
        self.dataframe = None
        self.random_state = None

    def fit(self, k=None):
        if k is not None:
            self.k = k
        self.model = KMeans(n_clusters=self.k, random_state=self.random_state).fit(self.dataframe[['latitude', 'longitude']])

    def predict(self, input_data):
        self.model.predict(input_data)