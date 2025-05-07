import requests
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import numpy as np
import matplotlib.pyplot as plt

start1 = float(input("start location lats: "))
start2 = float(input("start location lons: "))
finish1 = float(input("finish location lats: "))
finish2 = float(input("finish location lons: "))

start = (start1, start2)
end = (finish1, finish2)

step = int(input("resulation steps: "))
steps = step
lats = np.linspace(start[0], end[0], steps)
lons = np.linspace(start[1], end[1], steps)
coords = list(zip(lats, lons))

url = 'https://api.open-elevation.com/api/v1/lookup'
response = requests.post(url, json={'locations': [{'latitude': lat, 'longitude': lon} for lat, lon in coords]})
elevations = [point['elevation'] for point in response.json()['results']]

gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

for lat, lon, ele in zip(lats, lons, elevations):
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))

#Results
with open("elevation_path.gpx", "w") as f:
    f.write(gpx.to_xml())

distances = [0]
for i in range(1, len(coords)):
    d = geodesic(coords[i - 1], coords[i]).meters
    distances.append(distances[-1] + d)

plt.figure(figsize=(10, 5))
plt.plot(distances, elevations, marker='o', linestyle='-', color='green')
plt.title("Elevation Profile")
plt.xlabel("Distance along path (meters)")
plt.ylabel("Elevation (meters)")
plt.grid(True)
plt.tight_layout()
plt.savefig("elevation_profile.png")
plt.show()
