import logging
from PIL import Image
import io
import folium


def normalize_lat_lon(df):
    """
    Normalize column names in a DataFrame to 'latitude' and 'longitude'.
    
    Args:
        df (pd.DataFrame): Input DataFrame with latitude/longitude variations.

    Returns:
        pd.DataFrame: DataFrame with standardized 'latitude' and 'longitude' column names.
    """
    column_mapping = {
        "latitude": ["latitude", "lat", "ltd"],
        "longitude": ["longitude", "long", "lng"]
    }
    

    lowercase_cols = {col.lower(): col for col in df.columns}
    
    rename_dict = {}
    for standard_name, variations in column_mapping.items():
        for variant in variations:
            if variant in lowercase_cols:
                rename_dict[lowercase_cols[variant]] = standard_name
                break  
    
    return df.rename(columns=rename_dict)


def map_creator(input_map: folium.Map, request):
    """
    Saves the map as an image after adjusting the zoom level dynamically 
    to fit all clusters.

    Args:
        input_map (folium.Map): The map object.
        rqeuest: Request containing the name and the output dir of the image file.
    """

    marker_coords = []
    for child in input_map._children.values():
        if isinstance(child, folium.Marker):
            marker_coords.append(child.location)
    
    if marker_coords:
        input_map.fit_bounds(marker_coords)

    img_data = input_map._to_png(1) 
    img = Image.open(io.BytesIO(img_data))
    img.save(f'{request.output_dir}{request.name}_bus_map.png')

    logging.info(f"Map saved for {request.name} with adjusted bounds.")