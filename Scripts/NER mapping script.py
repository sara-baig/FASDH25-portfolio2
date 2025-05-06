import pandas as pd
import plotly.express as px

#Loading data files
counts_df = pd.read_csv("../ner_counts.tsv", sep="\t")
coords_df = pd.read_csv("../ner_gazetteer.tsv", sep="\t")

print("Counts columns:", counts_df.columns)
print("Coords columns:", coords_df.columns)

#Merging both dataframes on placenames
merged_df = pd.merge(counts_df, coords_df, left_on="Place", right_on="Name", how="inner")
#Cleaning the data by removing rows with missing coordinates or count
clean_df = merged_df.dropna(subset=["Latitude", "Longitude", "Count"]).copy()

#Converting columns to float safely
clean_df["Latitude"] = clean_df["Latitude"].astype(float)#help from ChatGPT
clean_df["Longitude"] = clean_df["Longitude"].astype(float)
clean_df["Count"] = clean_df["Count"].astype(float)  # this line prevents NaN in marker size

#Creating the map
fig = px.scatter_geo(
    clean_df,
    lat="Latitude",
    lon="Longitude",
    color="Place",
    hover_name="Place",
    size="Count", 
    projection="natural earth",
    size_max=20,
    title="NER-extracted Places (Jan 2024)"
)

#Exporting the map as PNG and HTML
fig.write_html("ner_map.html")
fig.write_image("ner_map.png")

print("Map files saved as 'ner_map.html' and 'ner_map.png'")
