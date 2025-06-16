import time
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from concurrent.futures import ProcessPoolExecutor
import os

def buffer_geom(geom, distance=0.05):
    return geom.buffer(
        distance,
        resolution=2,
        cap_style=2,
        join_style=2
    )

start_time = time.time()

print("Loading coastline shapefile...")
coast_fp = "data/AU_AIMS_Coastline_50k_2024/Simp/AU_NESP-MaC-3-17_AIMS_Aus-Coastline-50k_2024_V1-1_simp.shp"
gdf = gpd.read_file(coast_fp)

print("Buffering features in parallel...")
with ProcessPoolExecutor() as executor:
    buffered_geoms = list(executor.map(buffer_geom, gdf.geometry))

print("Unioning buffered geometries...")
buffered_union = gpd.GeoSeries(buffered_geoms).unary_union

print("Unioning all original features...")
coast_union = gdf.geometry.union_all()

print("Clipping off land (difference)...")
near_coast = buffered_union.difference(coast_union)

print("Simplifying geometry...")
near_coast_simple = near_coast.simplify(0.001)

print("Preparing output GeoDataFrame...")
if isinstance(near_coast_simple, (Polygon, MultiPolygon)):
    out_gdf = gpd.GeoDataFrame(geometry=[near_coast_simple], crs=gdf.crs)
else:
    out_gdf = gpd.GeoDataFrame(geometry=list(near_coast_simple), crs=gdf.crs)

print("Saving to shapefile...")
out_fp = "output/04/near-coast-mask.shp"
os.makedirs(os.path.dirname(out_fp), exist_ok=True)
out_gdf.to_file(out_fp)

print(f"Script completed in {time.time() - start_time:.2f} seconds.")
