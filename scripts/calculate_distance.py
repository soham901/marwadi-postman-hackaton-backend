import httpx
from geopy.distance import geodesic


def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


# Fetch the JSON data
response = httpx.get("http://localhost:8000/hospitals/")
hospitals = response.json()

# Calculate distances
for i, hospital1 in enumerate(hospitals):
    for j, hospital2 in enumerate(hospitals):
        if i < j:  # Avoid calculating the same pair twice
            distance = calculate_distance(
                hospital1["latitude"],
                hospital1["longitude"],
                hospital2["latitude"],
                hospital2["longitude"],
            )
            print(
                f"Distance between {hospital1['name']} and {hospital2['name']}: {distance:.2f} km"
            )
