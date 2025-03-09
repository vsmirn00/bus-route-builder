from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Optional, Tuple
import osmnx as ox
import networkx as nx
import folium
from folium import plugins
import numpy as np


def print_solution(manager, routing, solution, names=None):
    """
    Prints the solution on the console.

    Args:
        manager: The routing index manager.
        routing: The routing model.
        solution: The solution obtained from the routing solver.
        names (Optional[List[str]]): List of names corresponding to node indices. Defaults to None.
    """
    index = routing.Start(0)
    plan_output = "Route for vehicle:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        idx = manager.IndexToNode(index)
        if names:
            print_value = names[idx]
        else:
            print_value = idx
        plan_output += " {} ->".format(print_value)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

    idx = manager.IndexToNode(index)
    if names:
        print_value = names[idx]
    else:
        print_value = idx

    return route_distance / 1000 



def optimize_routes(
    distance_matrix: List[List[int]], depot: int, names: Optional[List[str]] = None
) -> List[int]:
    """
    Solves the vehicle routing problem and returns the optimized route.

    Args:
        distance_matrix (List[List[int]]): 2D list representing the distance matrix between nodes.
        depot (int): Index of the depot (starting point).
        names (Optional[List[str]]): List of names corresponding to node indices. Defaults to None.

    Returns:
        List[int]: The optimized route as a list of node indices.
    """
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix), 1, depot
    )  # num of vehicles set to 1

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console and return the optimized route.
    if solution:
        distance_solution = print_solution(manager, routing, solution, names)
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route, distance_solution
    else:
        return []


def plot_route(
    coordinates: List[Tuple[float, float]], dist: float = 1000, zoom_start: int = 15, mymap: folium.Map = None,
    input_color: str = "blue", central_station:bool = True
) -> folium.Map:



    median_tuple = tuple(np.median(np.array(coordinates), axis=0))

    distances = [
        np.linalg.norm(np.array(t) - np.array(median_tuple)) for t in coordinates
    ]

    closest_index = np.argmin(distances)

    closest_tuple = coordinates[closest_index]
    
    graph = ox.graph_from_point(
        center_point=closest_tuple, dist=dist, network_type="drive"
    )

    map_center = closest_tuple
    if mymap is None:
        mymap = folium.Map(
            location=map_center, zoom_start=zoom_start, tiles="cartodbpositron"
        )
    
    end_nodes = []
    # Plot the route between each pair of consecutive coordinates
    num_stops = len(coordinates)
    for i in range(num_stops - 1):
        start_node = ox.distance.nearest_nodes(
            graph, coordinates[i][1], coordinates[i][0]
        )
        end_node = ox.distance.nearest_nodes(
            graph, coordinates[i + 1][1], coordinates[i + 1][0]
        )
        route = nx.shortest_path(graph, start_node, end_node, weight="length")
        route_coordinates = [
            (graph.nodes[node]["y"], graph.nodes[node]["x"]) for node in route
        ]

        route_polyline = folium.PolyLine(locations=route_coordinates, color="red")
        mymap.add_child(route_polyline)

        ant_path = plugins.AntPath(
            locations=route_coordinates,
            color=input_color,
            dash_array=[10, 50],
            delay=500,
            weight=5,
        )
        mymap.add_child(ant_path)
        end_nodes.append(route_coordinates[-1])
    

    for coordinate in end_nodes:
        folium.Marker(
            location=coordinate, icon=folium.Icon(color="blue", icon="store")
        ).add_to(mymap)


    return mymap

