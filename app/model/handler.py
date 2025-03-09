from __future__ import print_function
import logging
from app.model.abstract_base_class import AbstractBaseClass
import scipy.cluster.hierarchy as sch
from sklearn.metrics import calinski_harabasz_score
from app.src.api_osmr import get_matrix, parse_coordinates
from app.src.routing import optimize_routes, plot_route

from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import calinski_harabasz_score

import pandas as pd
import numpy as np

from typing import List
from sklearn.cluster import MiniBatchKMeans
from scipy.spatial.distance import cdist
from loguru import logger

from app.utils.soft_colors import SOFT_COLORS



class ModelHandler(AbstractBaseClass):
    """
    Handles data loading, clustering, and centroid computations for route optimization.
    """
    
    def __init__(self):
        pass

    def load_data(self, path):
        """
        Loads input data from a CSV file.

        Parameters
        ----------
        path : str
        Path to the CSV file containing latitude and longitude data.
        """
        logger.info(f"Loading data from {path}")
        self.input_data = pd.read_csv(path)
        self.X = self.input_data[["Latitud", "Longitud"]].values
        self.soft_colors = SOFT_COLORS
        logger.info("Data loaded successfully")


    def find_max_diff(self, input_dictionary: dict, diff_value=1) -> int:
        """
        Finds the number of clusters (k) that maximizes the difference between 
        consecutive Calinski-Harabasz scores.

        Parameters:
        input_dictionary (dict): Keys are cluster numbers (k), values are CH scores.

        Returns:
        int: Optimal number of clusters (k) based on the maximum difference.
        """
        
        sorted_k = sorted(input_dictionary.keys())

        differences = {k: input_dictionary[k] - input_dictionary[sorted_k[i - 1]]
                    for i, k in enumerate(sorted_k[1:], start=1)}

        return max(differences, key=differences.get) - diff_value

    
    def find_best_n_clusters(self, linked, data, min_clusters=20, max_clusters=30, diff_value=1) -> int:
        """Find the best number of clusters based on the max difference between the calinski-harabasz scores"""

        scores_dict = {}

        for k in range(min_clusters, max_clusters):  
            labels = fcluster(linked, k, criterion='maxclust') 
            scores_dict[k] = calinski_harabasz_score(data, labels)

        return self.find_max_diff(scores_dict, diff_value=diff_value)


    def compute_cluster_centroids(self, data, labels):
        """Computes and returns the cluster centroids in the format of np.array"""
        unique_clusters = np.unique(labels)
        centroids = []

        for cluster in unique_clusters:
            cluster_points = data[labels == cluster] 
            centroid = cluster_points.mean(axis=0)  
            centroids.append(centroid)

        return np.array(centroids)

        
        
    def balanced_kmeans_labels(self, df, num_routes=3, num_stations_per_route=9):
        """
        Cluster bus stations into balanced groups with equal number of points.

        Args:
            df (DataFrame): DataFrame with columns ['lat', 'lng'].
            num_routes (int): Number of bus routes.
            num_stations_per_route (int): Number of bus stations per route.

        Returns:
            List[int]: List of cluster labels (0, 1, 2) corresponding to input data order.
        """

        
        kmeans = MiniBatchKMeans(n_clusters=num_routes, random_state=42, n_init=10)
        labels = kmeans.fit_predict(df[["lat", "lng"]])

        # Step 2: Balance the Clusters
        df_temp = df.copy()
        df_temp["route_id"] = labels

        max_iterations = 100
        iteration = 0
        while iteration < max_iterations:
            route_counts = df_temp["route_id"].value_counts().to_dict()
            if all(count == num_stations_per_route for count in route_counts.values()):
                break
            iteration += 1

            
            oversized_clusters = {r: c for r, c in route_counts.items() if c > num_stations_per_route}
            undersized_clusters = {r: c for r, c in route_counts.items() if c < num_stations_per_route}

            
            for over_cluster, over_count in oversized_clusters.items():
                excess_points = over_count - num_stations_per_route
                over_points = df_temp[df_temp["route_id"] == over_cluster][["lat", "lng"]].values

                
                for under_cluster, under_count in undersized_clusters.items():
                    under_centroid = df_temp[df_temp["route_id"] == under_cluster][["lat", "lng"]].mean().values.reshape(1, -1)
                    distances = cdist(over_points, under_centroid)

                    
                    move_indices = df_temp[df_temp["route_id"] == over_cluster].index[np.argsort(distances.flatten())[:excess_points]]
                    df_temp.loc[move_indices, "route_id"] = under_cluster

        return df_temp["route_id"].tolist()
    

    def generate_central_station(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a central bus station (mean of all latitude and longitude) to the dataframe.

        Args:
            df (pd.DataFrame): DataFrame with 'lat' and 'lng' columns.

        Returns:
            pd.DataFrame: Updated DataFrame with an additional central station.
        """
        tmp_lng = np.mean(df["lng"])
        tmp_lat = np.mean(df["lat"])
        tmp_df = pd.DataFrame([{"bus_stop":-1, "lat": tmp_lat, "lng":tmp_lng, "route_id":-1}])
        output_df = pd.concat([tmp_df, df]) 
        return output_df
    

    def create_k_dataframes(self, original_df:pd.DataFrame) -> List:
        """
        Creates separate DataFrames for each route, including the central station.

        Parameters
        ----------
        original_df : pd.DataFrame
            The DataFrame containing bus stops and routes.

        Returns
        -------
        list
            A list of DataFrames, one for each route.
        """
       
        route_ids = original_df["route_id"].unique().tolist()

        df_list = [original_df[(original_df["route_id"] == route_id) | (original_df["route_id"] == -1)] for route_id in route_ids if route_id >= 0]

        return df_list
    
    
    def ensure_index_starts_at_zero(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensures that the DataFrame index starts at 0. If 0 is missing, 
        renumbers the index so the first row gets index 0.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame with adjusted index.
        """
        if 0 not in df.index:
            df = df.reset_index(drop=True) 
        return df


    def create_input_df(self):
        """
        Creates the input DataFrame by clustering station and route centroids.

        Uses hierarchical clustering to determine station and route clusters,
        then assigns each station to the nearest route cluster.
        
        Returns
        -------
        None
        """

        route_labels = fcluster(self.linked, self.num_routes, criterion='maxclust')
        station_labels = fcluster(self.linked, self.num_stations, criterion='maxclust')


        station_centroids = self.compute_cluster_centroids(self.X, station_labels)
        route_centroids = self.compute_cluster_centroids(self.X, route_labels)


        self.df = pd.DataFrame(data=station_centroids, columns=["lat", "lng"]).reset_index(names="bus_stop") 
        self.df["bus_stop"] = self.df["bus_stop"].astype(str)  


        route_assignments = []
        for station in station_centroids:
            distances = cdist([station], route_centroids) 
            closest_route = np.argmin(distances)  
            route_assignments.append(closest_route)

        self.df["route_id"] = route_assignments 

    
    def optimization_wrapper(self, df: pd.DataFrame):
        """
        Wrapper function for route optimization.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing bus stop locations.

        Returns
        -------
        list
            Optimized route order for bus stops.
        """
        logger.info("Starting route optimization")
        df = self.ensure_index_starts_at_zero(df)
        bus_stops_list = df.bus_stop
        coordinates = parse_coordinates(df)

        response_distances = get_matrix(coordinates)

        distances = np.array(response_distances["distances"]).astype(int)
        starting_stop = df["bus_stop"].iloc[0]

        depot_index = int(bus_stops_list.index[bus_stops_list == starting_stop][0])
        return optimize_routes(distances, depot_index, list(bus_stops_list))



    def map_wrapper(self, df: pd.DataFrame, idx_route, input_color):
        """
        Wrapper function for generating route maps.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing bus stop locations.
        idx_route : list
            Index order for the optimized route.
        input_color : str
            Color for the plotted route.

        Returns
        -------
        folium.Map
            Map with the plotted route.
        """
        logger.info("Generating route map")

        df_best_route = df.iloc[idx_route[0]]

        coordinates = list(zip(df_best_route["lat"], df_best_route["lng"]))

        return plot_route(coordinates, dist=30000, zoom_start=11, input_color=input_color)


    def fit(self, path, num_stations = None, balance_stations=True, generate_central_station=True, num_routes=None, method="ward"):
        """
        Fits the hierarchical clustering model and assigns stations to routes.

        Parameters
        ----------
        path : str
            Path to input data.
        num_stations : int, optional
            Number of stations (default is None).
        balance_stations : bool, optional
            Whether to balance stations using k-means (default is True).
        generate_central_station : bool, optional
            Whether to add a central station (default is True).
        num_routes : int, optional
            Number of routes (default is None).
        method : str, optional
            Clustering method to use (default is "ward").

        Returns
        -------
        None
        """
        logger.info("Starting fit function")

        # HCA
        self.num_stations  = num_stations
        self.num_routes = num_routes
        self.load_data(path)
        self.linked = sch.linkage(self.X, method=method)
        
        # The first clustering is to find group the POI into a a single cluster
        if self.num_stations == 0:
            self.num_stations = self.find_best_n_clusters(linked=self.linked, data=self.X)
        logger.info(f"Num of bus stations: {self.num_stations}") 


        # Cut the dendogram
        # The second is to find the optimal number of routes
        if self.num_routes == 0:
            self.num_routes = self.find_best_n_clusters(self.linked, self.X, min_clusters=2, max_clusters=6, diff_value=0)
        
        else:
            logger.info(f"Setting number of routes: {self.num_routes}") 

        # We set the input df 
        self.create_input_df() 

        if balance_stations==True:
            self.df["route_id"] = self.balanced_kmeans_labels(self.df) 
            logger.info("generating labels with kmeans to balance the number of stations")
        
        else:
            logger.info("Not balancing number of stations")


        if generate_central_station == True:
            self.df = self.generate_central_station(self.df)
            logger.info("generating central station")

        else:
            logger.info("Not generating central station")
        
        
        self.k_df_list = self.create_k_dataframes(self.df)



    def predict(self, request, method="ward"):
        """
        Runs the full pipeline for predicting optimized routes and generating maps.

        Parameters
        ----------
        request : object
            Request object containing input parameters.
        method : str, optional
            Clustering method to use (default is "ward").

        Returns
        -------
        tuple
            - list: Optimized routes.
            - list: Route maps.
        """
        logger.info("Starting prediction process")
        self.fit(path=request.input_path, num_stations=request.num_stations, balance_stations=request.balance_stations, generate_central_station=request.central_station, num_routes=request.num_routes, method=method)

        optimized_routes = [self.optimization_wrapper(route) for route in self.k_df_list]
        logger.info("Finished optimization_wrapper")

        optimized_maps = [self.map_wrapper(self.k_df_list[i], optimized_routes[i], self.soft_colors[i]) for i in range(len(self.k_df_list))]
        logger.info("Finished map_wrapper")

        return optimized_routes, optimized_maps
