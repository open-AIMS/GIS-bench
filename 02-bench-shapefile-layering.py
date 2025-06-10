"""
Combine and flatten habitat polygon layers into a single shapefile with correct stacking order.

This script processes a set of habitat polygon shapefiles, each representing a different habitat type
and digitised with an assumed stacking order (e.g., Asphalt on top, Marine feature (Rock) on bottom).
The script combines these layers into a single output shapefile, ensuring that overlaps are removed
according to the stacking order: each lower layer is clipped by the union of all layers above it.

Algorithm:
1. Define the stacking order and corresponding shapefile for each habitat type.
2. For each layer, from top to bottom:
    a. Read the shapefile and ensure it uses the target CRS (EPSG:4326).
    b. Clip the current layer by the union of all previously processed (higher) layers.
    c. Add the clipped features to the output GeoDataFrame, tagging each with its habitat type.
    d. Update the union of all processed layers for use in the next iteration.
3. Save the combined, non-overlapping polygons to a new shapefile, with a 'Type' attribute indicating habitat.
4. Print timing information for each layer and the total process.

This approach avoids redundant digitising of boundaries between stacked habitats and produces a clean,
flattened habitat map suitable for further analysis or mapping.

Requirements:
- geopandas
- shapely
- pandas
"""

import geopandas as gpd
from shapely.ops import unary_union
import os
import pandas as pd
import time

input_dir = "data/habitat/habitat-raw"

layers = [
    ("Asphalt", "Keppel_Other-2.shp"),
    ("Buildings", "Keppel_Other-1.shp"),
    ("Mangroves", "Keppel_Veg-7.shp"),
    ("Cabbage-tree palm (Livistonia)", "Keppel_Veg-6.shp"),
    ("Sheoak (Casuarina)", "Keppel_Veg-5.shp"),
    ("Other vegetation", "Keppel_Veg-4.shp"),
    ("Grass", "Keppel_Veg-3.shp"),
    ("Salt flat", "Keppel_Veg-2.shp"),
    ("Rock", "Keppel-7.shp"),
    ("Beach rock", "Keppel-6.shp"),
    ("Gravel", "Keppel-5.shp"),
    ("Coral", "Keppel-4.shp"),
    ("Sparse coral", "Keppel-3.shp"),
    ("Unknown not rock (Macroalgae on rubble)", "Keppel-2.shp"),
    ("Marine feature (Rock)", "Keppel-1.shp"),
]

output_dir = "output/02"
os.makedirs(output_dir, exist_ok=True)
output_shp = os.path.join(output_dir, "Keppels_AIMS_Habitat-mapping_2019.shp")

final_gdf = gpd.GeoDataFrame(columns=["Type", "geometry"], crs="EPSG:4326")
progressive_dissolve = None

# Start timing the entire process
total_start_time = time.time()

print("This test takes approximately 10 - 15 minutes. Please be patient...")
for name, file in layers:
    # Start timing this layer
    layer_start_time = time.time()
    print(f"Processing {name}...")
    path = os.path.join(input_dir, file)
    gdf = gpd.read_file(path)
    gdf = gdf[gdf.geometry.notnull()]
    gdf = gdf.to_crs("EPSG:4326")  # Ensure all layers use the same CRS
    gdf["Type"] = name

    if progressive_dissolve is not None and not progressive_dissolve.is_empty.any():
        clipped = gpd.overlay(gdf, progressive_dissolve, how="difference")
    else:
        clipped = gdf.copy()

    final_gdf = pd.concat([final_gdf, clipped[["Type", "geometry"]]], ignore_index=True)

    if progressive_dissolve is None:
        progressive_dissolve = gdf[["geometry"]].copy()
    else:
        union_geom = unary_union(list(progressive_dissolve.geometry) + list(gdf.geometry))
        progressive_dissolve = gpd.GeoDataFrame(geometry=[union_geom], crs="EPSG:4326")
    # End timing for this layer
    layer_end_time = time.time()
    layer_elapsed_time = layer_end_time - layer_start_time
    print(f"  Completed in {layer_elapsed_time:.2f} seconds")

final_gdf.to_file(output_shp)
print(f"Saved to {output_shp}")
# Calculate and display total processing time
total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time
print(f"\nTotal processing time: {total_elapsed_time:.2f} seconds ({total_elapsed_time/60:.2f} minutes)")