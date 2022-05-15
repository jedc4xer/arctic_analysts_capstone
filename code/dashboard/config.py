import json

database = "arctic_analysts_capstone"
table = "table_name"  # This will be variable
user = "arctic_analysts"
password = "ThisPassw0rd!"
server = "gen10-data-fundamentals-22-02-sql-server.database.windows.net"

with open("2021_US_Counties_3.7.json") as file:
    counties = json.load(file)
    file.close()

print("Loaded County JSON file.")
