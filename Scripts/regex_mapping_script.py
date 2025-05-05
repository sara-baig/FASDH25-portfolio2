import pandas as pd
import plotly.express as px


#loading gazeeteer data into dataframe
gazetteer_path="../gazetteers/geonames_gaza_selection.tsv"
gazetteer_df=pd.read_csv(gazetteer_path, sep="\t")

#loading frequency tsv
regex_df=pd.read_csv("regex_counts.tsv", sep="\t")

regex_df["placename"] = regex_df["placename"].str.lower()#took help from ChatGPT
gazetteer_df["asciiname"] = gazetteer_df["asciiname"].str.lower()

regex_df["placename"] = regex_df["placename"].str.strip()
gazetteer_df["asciiname"] = gazetteer_df["asciiname"].str.strip()


#merging the two dataframes which do not have any column in common 
merged_df = pd.merge(regex_df, gazetteer_df, left_on="placename", right_on="asciiname", how="inner")#help from ChatGPT
print(merged_df)

## Display the merged dataframe (using color to represent frequency)
fig = px.scatter_map(merged_df, lat="latitude", lon="longitude", hover_name="asciiname", color="count", color_continuous_scale=px.colors.sequential.YlOrRd)
fig.update_layout(map_style="carto-darkmatter-nolabels")
fig.show()

# configures the map background:
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


fig.update_layout(
    title="frequency over time",
    title_font_size=20,
    geo=dict(
        showland=True, landcolor="lightgreen",
        showocean=True, oceancolor="lightblue",
        showrivers=True, rivercolor="blue"
        )
    )

fig.show()


# saves the interactive map as html
fig.write_html("regex_map.html")
