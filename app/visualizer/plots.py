import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import folium

def plot_path(points, best_path, n_points):
    plt.figure(figsize=(8, 6))
    plt.scatter(points[:,0], points[:,1], c='r', marker='o', label='Points')
        
    for i in range(n_points-1):
        plt.plot([points[best_path[i],0], points[best_path[i+1],0]],
                [points[best_path[i],1], points[best_path[i+1],1]],
                c='g', linestyle='-', linewidth=2, marker='o')
            
    plt.plot([points[best_path[0],0], points[best_path[-1],0]],
            [points[best_path[0],1], points[best_path[-1],1]],
            c='g', linestyle='-', linewidth=2, marker='o', label='Best Path')
        
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Ant Colony Optimization')
    plt.show()

def plot_on_map(df, centers=None, best_path=None, location=(59.93863, 30.31413), zoom_start=8):
    m = folium.Map(location=location, 
                   zoom_start=zoom_start
                   )

    folium.TileLayer("openstreetmap").add_to(m)
    figure = folium.FeatureGroup(name="Cities and Clusters").add_to(m)

    unique_clusters = df['cluster_label'].unique()
    colormap = cm.get_cmap('tab10', len(unique_clusters))
    cluster_colors = {cluster: mcolors.to_hex(colormap(i)) for i, cluster in enumerate(unique_clusters)}

    for _, row in df.iterrows():
        cluster_label = row['cluster_label']
        color = cluster_colors[cluster_label] 
        simplified = row['geometry'].simplify(tolerance=0.01, preserve_topology=True)
        
        folium.GeoJson(
            simplified,
            style_function=lambda x, color=color: {'fillColor': color, 'color': color, 'weight': 1, 'fillOpacity': 0.5},
            tooltip=f"Cluster: {cluster_label}" 
        ).add_to(figure)

    if centers is not None:
        for idx, center in enumerate(centers):
            folium.Marker(
                (center[0], center[1]),
                tooltip=f"Cluster Centroid {idx}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(figure)

    # Plot the best path
    if best_path is not None and centers is not None:
        path_coordinates = [(centers[idx][0], centers[idx][1]) for idx in best_path]
        folium.PolyLine(
            path_coordinates,
            color="red",
            weight=2,
            opacity=0.8,
            tooltip="Optimized Path"
        ).add_to(figure)

    folium.LayerControl(collapsed=False).add_to(m)

    return m
