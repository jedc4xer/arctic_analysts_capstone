import json

database = "arctic_analysts_capstone"
table = "table_name"  # This will be variable
user = "arctic_analysts"
password = "ThisPassw0rd!"
server = "gen10-data-fundamentals-22-02-sql-server.database.windows.net"

# New Jersey GEOJSON from https://njogis-newjersey.opendata.arcgis.com/datasets/county-boundaries-of-nj/explore?location=40.273633%2C-72.892608%2C8.33
# Reshaped with Mapshaper

with open("shapefiles/County_Boundaries_of_NJ.json") as file:
    counties = json.load(file)
    file.close()
print("Loaded County JSON file.")
