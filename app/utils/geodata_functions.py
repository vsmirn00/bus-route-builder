import io
import logging
from PIL import Image

def extract_coordinates(polygon):
    """
    Extracts the coordinates from a shapely.geometry.Polygon object.
    
    Parameters:
        polygon (shapely.geometry.Polygon): The Polygon object.
        
    Returns:
        list of tuples: A list of (longitude, latitude) tuples.
    """
    if polygon.is_empty:
        return []  # Return empty list for empty geometries
    
    return list(polygon.exterior.coords)


def get_longitude_latitude(df):

    tmp_lst = [value['coordinates'][0] for idx, value in df.iterrows()]
    df['longitude'] = [value[0] for value in tmp_lst]
    df['latitude'] = [value[1] for value in tmp_lst]
    return df 


def map_creator(input_map, name):
    img_data = input_map._to_png(1)
    img = Image.open(io.BytesIO(img_data))
    img.save(f'output_folder/{name}_bus_map.png')
    logging.info(f"Map saved for {name}")