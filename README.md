# Zesty.ai Backend Project - Code for Containerized Service

## Summary
Returns basic information about a given property and its neighbors<br>
The complete containerized service can be found at related repo: https://github.com/suejungshin/zesty-api

## How to Run

### For Local Development
`docker-compose up -d` <br>
When developing locally:<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
`pip3 install -r requirements.txt`<br>
`python3 index.py`

### For PRODUCTION
`docker-compose -p project up -d` ("-p project" so container name is predictable for steps below, "-d" for detatched mode)

Naviate to services:

http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610?overlayed=true
http://localhost:8080/api/statistics/622088210a6f43fca2a1824e8610df03?distance=10
```
curl --location --request POST 'http://localhost:8080/api/find' \
--header 'Content-Type: application/json' \
--data-raw '{
"type": "Feature",
"geometry": {
"type": "Point",
"coordinates": [-80, 26]
},
"distance_meters": 10000000
}'
```

## How To Test

### For Local Development
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
`pytest`<br>

In addition, can go to links at localhost below to check it out.<br>
Here are the valid propertyIDs for the 5 properties in the test database, for reference:
- f1650f2a99824f349643ad234abff6a2
- f853874999424ad2a5b6f37af6b56610
- 3290ec7dd190478aab124f6f2f32bdd7
- 5e25c841f0ca47ac8215b5fd0076259a
- 622088210a6f43fca2a1824e8610df03

### For Production
`docker exec -it project_zesty_app_1 pytest`<br>
(or grab CONTAINER ID for the zesty_app at port 8080 printed from `docker ps -a` and subsitute, e.g., `docker exec -it 9c270f7860ac pytest`)

### To Access Postgres shell from within Docker container:
1. `docker-compose up -d` (if not already done above)
2. `docker exec -it project_postgres_1 psql -U postgres`
or `docker exec -it 9c270f7860ac psql -U postgres` where the alphanumeric string should be replaced by the container ID from running `docker ps -a`
(If developing locally, need to `docker stop project_zesty_app_1` the dockerized zesty_app service and serve it at local host and keep the dockerized postgres db running)

### How To Build Image
To build image:<br>
`docker build -t zesty .`<br>
`docker images` Get image id<br>
`docker tag INSERT_IMAGE_ID_HERE suejungshin/zesty-app:latest`<br>
`docker push suejungshin/zesty-app:latest`<br>

## API endpoints

Endpoints are exposed at http://localhost:8080/{endpoint}

  ### GET /api/display/:id(?overlayed=True)

  Returns the image of the property by ID

  Path parameter - property ID (e.g., f853874999424ad2a5b6f37af6b56610)<br>
  Query parameter (optional) - overlayed=True or overlayed=False (case insensitive)

  Examples -
  http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610
  http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610?overlayed=true
  http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610?overlayed=false

  Example response:<br>
  JPEG image as displayed in browser<br>
  If overlay is true, image has overlayed building and parcel polygons


  ### POST /api/find

  Returns list of property IDs that are within search distance radius (in METERS) of the target property. Note that distances are based on distance between each property's POINT geocode_code which is at the center of each property.

  POST a geojson object specifying [longitude, latitude] (in DEGREES) of target property, as well as search distance radius in METERS<br>

  Example- http://localhost:8080/api/find  (plus the POST data below)<br>
  POST request data must be in format:
   ```python
  {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [-80, 26]
    },
    "distance_meters": 1000000
  }
  ```

  Example response:
  ```python
  ['f853874999424ad2a5b6f37af6b56610', '3290ec7dd190478aab124f6f2f32bdd7', '622088210a6f43fca2a1824e8610df03']
  ```

  Note that the PostGIS query seems to break down at distances too large, in which case the API response will be "Search distance too large"

  ### GET /api/statistics

  Returns basic statistics about the target property's neighbors, where neighbors are those properties whose POINT geocode_code are within target distance (in METERS) of the target property's POINT geocode_code:
  - Total area (in SQUARE METERS) of all neighboring parcels, summed
  - List of areas (in SQUARE METERS) of neighboring buildings
  - List of distances (in METERS) between each neighboring building (POLYGON) and target property (POINT geocode_geo). The ST_Distance function used finds the minimum 2D Cartesian distance, so looks to the closest part on the edge of the building polygon.
  - Zone density (in PERCENT, so a result of 100 means 100% and a result of 0.1 means 0.1%) - percent of buffer of target distance around the target property that is occupied by a building

  Path parameter - property ID (e.g., f853874999424ad2a5b6f37af6b56610)<br>
  Query parameter - distance in METERS

  Example -
  http://localhost:8080/api/statistics/622088210a6f43fca2a1824e8610df03?distance=10

  Example response:
```python
  {
    total_parcel_area_in_radius: 2330.55982263293,
    buildings_areas: [
      981.199068874121
    ],
    buildings_dists_to_center: [
      0
    ],
    zone_density: 97.49789007556822
  }
```
