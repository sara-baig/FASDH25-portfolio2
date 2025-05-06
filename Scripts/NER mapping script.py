import pandas as pd
import plotly.express as px

# Step 1: Load the data files
counts_df = pd.read_csv("ner_counts.ipynb", sep="\t")
coords_df = pd.read_csv("build_gazetteer.ipynb", sep="\t")

# Step 2: Merge both dataframes on placename
merged_df = pd.merge(counts_df, coords_df, left_on="place", right_on="name", how="inner")

# Step 3: Clean the data by removing rows with missing coordinates or count
clean_df = merged_df.dropna(subset=["latitude", "longitude", "count"]).copy()

# Step 4: Convert columns to float safely
clean_df["latitude"] = clean_df["latitude"].astype(float)
clean_df["longitude"] = clean_df["longitude"].astype(float)
clean_df["count"] = clean_df["count"].astype(float)  # this line prevents NaN in marker size

# Step 5: Create the map
fig = px.scatter_geo(
    clean_df,
    lat="latitude",
    lon="longitude",
    text="placename",
    size="count", 
    projection="natural earth",
    title="NER-extracted Places (Jan 2024)"
)

# Step 6: Export the map as HTML and PNG
fig.write_html("ner_map.html")
fig.write_image("ner_map.png")

print("Map files saved as 'ner_map.html' and 'ner_map.png'")
