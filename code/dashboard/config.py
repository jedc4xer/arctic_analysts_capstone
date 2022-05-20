import json

database = "arctic_analysts_capstone"
table = "table_name"  # This will be variable
user = "arctic_analysts"
password = "ThisPassw0rd!"
server = "gen10-data-fundamentals-22-02-sql-server.database.windows.net"

# New Jersey GEOJSON from https://njogis-newjersey.opendata.arcgis.com/datasets/county-boundaries-of-nj/explore?location=40.273633%2C-72.892608%2C8.33
# Reshaped with Mapshaper

feature_options = {
    "MedianHousePrice": "Median House Price",
    "MedianIncome": "Median Income",
    "NewBuildings": "New Buildings",
    "NewUnits": "New Units",
    "AverageRate": "Mortgage Rate",
}

locale_options = {
    "34001": "Atlantic County",
    "34003": "Bergen County",
    "34005": "Burlington County",
    "34007": "Camden County",
    "34009": "Cape May County",
    "34011": "Cumberland County",
    "34013": "Essex County",
    "34015": "Gloucester County",
    "34017": "Hudson County",
    "34019": "Hunterdon County",
    "34021": "Mercer County",
    "34023": "Middlesex County",
    "34025": "Monmouth County",
    "34027": "Morris County",
    "34029": "Ocean County",
    "34031": "Passaic County",
    "34033": "Salem County",
    "34035": "Somerset County",
    "34037": "Sussex County",
    "34039": "Union County",
    "34041": "Warren County",
}

age_groups = {
    "overall": "Overall",
    "under-25": "Under 25",
    "25-44": "25 to 44",
    "45-64": "45 to 64",
    "65-plus": "65 +",
}

base_maps = {
    "open-street-map": "Street Map",
    "carto-positron": "Positron",
    "carto-darkmatter": "Dark",
    "stamen-terrain": "Terrain",
    "stamen-toner": "Toner",
    "stamen-watercolor": "Watercolor",
}

with open("shapefiles/County_Boundaries_of_NJ.json") as file:
    counties = json.load(file)
    file.close()
