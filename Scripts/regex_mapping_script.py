import pandas as pd #import panda for tabular data
import plotly.express as px #import plotly for interactive mapping 


#load gazetteer path
gazetteer_path="../gazetteers/geonames_gaza_selection.tsv"
#loading gazeeteer data into dataframe
gazetteer_df=pd.read_csv(gazetteer_path, sep="\t")

#loading frequency data using regex
regex_df=pd.read_csv("regex_counts.tsv", sep="\t")

#convert place names to lowercase for standardizing for merging
regex_df["placename"] = regex_df["placename"].str.lower()#took help from ChatGPT(script 3)
gazetteer_df["asciiname"] = gazetteer_df["asciiname"].str.lower()

#remove whitespaces for avoiding mismatches
regex_df["placename"] = regex_df["placename"].str.strip()#cleas regex-extracted names
gazetteer_df["asciiname"] = gazetteer_df["asciiname"].str.strip()#clean gazetteer names


#merging the two dataframes which do not have any column in common 
merged_df = pd.merge(regex_df, gazetteer_df, left_on="placename", right_on="asciiname", how="inner")#help from ChatGPT
print(merged_df)#show output of merge to confirm coordinates

## Display a map showing placename frequencies using dot color intensity
fig = px.scatter_map(merged_df, lat="latitude", lon="longitude", hover_name="asciiname", color="count", color_continuous_scale=px.colors.sequential.YlOrRd)
fig.update_layout(map_style="carto-darkmatter-nolabels")
fig.show()

# configures the map background for clarity:
fig.update_geos(
    projection_type="natural earth",
    fitbounds="locations",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Brown",
    showocean=True, oceancolor="LightBlue",
    showlakes=False, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
    showcountries=False, countrycolor="Grey"
)
fig.show()

# Saves the map as a static image (PNG)
fig.write_image("regex_map.png", scale=2)

# Display the frequencies on a frame map per month:
fig = px.scatter_geo(merged_df, lat="latitude", lon="longitude", size="count", hover_name="asciiname", animation_frame="month", color="count", color_continuous_scale=px.colors.sequential.YlOrRd,  projection="natural earth")

#improve layout for map
fig.update_layout(
    title="frequency over time",
    title_font_size=20,
    geo=dict(
        showland=True, landcolor="lightgreen",
        showocean=True, oceancolor="lightblue",
        showrivers=True, rivercolor="blue"
        )
    )

#display the map 
fig.show() 


# saves the interactive map as html
fig.write_html("regex_map.html")
