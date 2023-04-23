import folium
import pandas as pd

# Read the CSV file
csv_file = "202304012238291fea.csv"
data = pd.read_csv(csv_file)

# Use only the first 100 entries in the CSV
data = data.head(100)

# Create a folium map centered at a specific latitude and longitude
latitude = 40.0
longitude = -89.0
m = folium.Map(location=[latitude, longitude], zoom_start=5.5)

# Iterate through the rows of the CSV file, adding markers for each location on the map
for index, row in data.iterrows():
    name = row["name"]
    lat = row["latitude"]
    lon = row["longitude"]
    rating = row["rating"]  # Retrieve the rating from the row
    phone = row["phone"]  # Retrieve the phone number from the row
    street = row["street"]  # Retrieve the street from the row
    
     # Create a string with the name, rating, phone, and full address with bold labels
    popup_content = f"<b>{name}</b><br><b>Rating:</b> {rating}<br><b>Phone:</b> {phone}<br><b>Address:</b> {street}"
    
    folium.Marker([lat, lon], popup=popup_content).add_to(m)  # Use the popup_content for the popup

# Display the map
