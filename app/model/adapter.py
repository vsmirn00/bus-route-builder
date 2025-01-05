import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from app.model.handler import ModelHandler

RANDOM_STATE = 42

class ModelAdapter(ModelHandler):
    def __init__(self, dataframe, k=None):
        self.k_means_adapter = ModelHandler()
        self.k_means_adapter.dataframe = dataframe
        self.random_state = RANDOM_STATE
        self.k_means_adapter.fit(k)
    
    def _get_labels(self):
        self.k_means_adapter.dataframe['cluster_label'] = self.k_means_adapter.model.labels_

    def return_updated_dataframe(self):
        self._get_labels()
        return self.k_means_adapter.dataframe
    
    def return_centers(self):
        return self.k_means_adapter.model.cluster_centers_
    
    def elbow_method(self):
        sse = {}
        for k in range(1, 10):
            kmeans = KMeans(n_clusters=k, max_iter=1000).fit(self.k_means_adapter.dataframe[['latitude', 'longitude']])
            self.k_means_adapter.dataframe["clusters"] = kmeans.labels_
            sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
        plt.figure()
        plt.plot(list(sse.keys()), list(sse.values()))
        plt.xlabel("Number of cluster")
        plt.ylabel("SSE")
        plt.show()