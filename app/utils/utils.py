from app.utils.geodata_functions import extract_coordinates, get_longitude_latitude
import geopandas as gpd # type: ignore

def df_factory(df):
    df = gpd.read_file(df)
    df['coordinates'] = df['geometry'].apply(extract_coordinates)
    df = get_longitude_latitude(df)
    df = df.drop(columns="coordinates")
    return df