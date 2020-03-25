# Zesty.ai Backend Project

## Summary

Returns basic information about a given property and its neighbors


## How to Run

1. `docker-compose -p project up -d` ("-p project" so container name is predictable for steps below, "-d" for detatched mode)
2. `docker exec -it project_zesty_app_1 pytest`
3. ` `


### To Run Tests:
1. `docker exec -it project_zesty_app_1 pytest` (or grab CONTAINER ID for the zesty_app at port 8080 printed from `docker ps -a` and subsitute )

Alternatively, can go to following example links in browser or Postman to see response:
http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610
Expected Reponse -
image from https://storage.googleapis.com/engineering-test/images/f853874999424ad2a5b6f37af6b56610.tif but as jpeg

http://localhost:8080/api/statistics/622088210a6f43fca2a1824e8610df03?distance=1000
Expected Response -
```python
{
total_parcel_area_in_radius: 2330.55982263293,
buildings_areas: [
981.199068874121
],
buildings_dists_to_center: [
0
],
zone_density: 3.1415629859896486
}
```

## API endpoints

Endpoints are exposed at http://localhost:8080/{endpoint}

  #### GET /api/display/:id

  Returns the image of the property by ID

  Path parameter - property ID (e.g., f853874999424ad2a5b6f37af6b56610)

  Example - http://localhost:8080/api/display/f853874999424ad2a5b6f37af6b56610

  Example response:
  JPEG image as displayed in browser


  #### POST /api/find

  Returns list of property IDs that are within search distance radius of the target property. Note that distances are based on POINT geocode_code which is the center of each property.

  POST a geojson object specifying [longitude, latitude] of target property, as well as search distance radius in METERS

  POST request data must be in format:

   ```python
  {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [-80, 26]
    },
    "distance": 1000000
  }
  ```

  Example response:
  ```python
  ['f853874999424ad2a5b6f37af6b56610', '3290ec7dd190478aab124f6f2f32bdd7', '622088210a6f43fca2a1824e8610df03']
  ```

  #### POST /api/statistics

  Returns list of property IDs that are within search distance radius of the target property. Note that distances are based on POINT geocode_code which is the center of each property.

  POST a geojson object specifying [longitude, latitude] of target property, as well as search distance radius in METERS

  POST request data must be in format:

   ```python
  {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [-80, 26]
    },
    "distance": 1000000
  }
  ```

  Example response:
  ```python
  ['f853874999424ad2a5b6f37af6b56610', '3290ec7dd190478aab124f6f2f32bdd7', '622088210a6f43fca2a1824e8610df03']
  ```


## Other Notes

Other Notes to Self:

##### To Access Postgres shell from within Docker container:
1. `docker-compose up -d` (if not already done above)
2. `docker ps -a`  Get the container ID (e.g., 9c270f7860ac)
3. `docker exec -it project_postgres_1 psql -U postgres` or `docker exec -it 9c270f7860ac psql -U postgres` where the alphanumeric string should be replaced by the container ID from above
(If developing locally, need to `docker stop project_zesty_app_1` the dockerized zesty_app service and serve at local host)

##### Basic Postgres commands:
`\l`  -- Show databases
`\c databaseName`  -- Connect to database of choice
`\dt` -- show tables
`\x` -- expanded view on to show rows in the case the column view wrapping poorly
`SELECT * FROM properties;`

Can run the ST_ commands in psql - make sure to use single quotes, not double quotes
`SELECT ST_AsEWKT('0101000020E6100000A79608AFB80454C08CEABEAD05633A40');`



Notes for my completed project!

#Engineering journal:

##To access postgres shell within Docker container:
`docker-compose up -d`  (-d for detached mode)
Get the container ID from running `docker ps -a`
`docker exec -it 9c270f7860ac psql -U postgres` where the alphanumeric string should be replaced by the container ID from above

\l  - show databases
\c databaseName  - connect to database of choice
\dt - show tables
\x - expanded view on to show rows in the case the column view wrapping poorly

SELECT * FROM properties;
SELECT ST_AsText('0101000020E6100000A79608AFB80454C08CEABEAD05633A40');


python3 -m venv venv
source venv/bin/activate
to get out `deactivate`

pip install flask-sqlalchemy psycopg2

to run --> python3 index.py  or FLASK_APP=index.py flask run

pip install -U pip
pip install psycopg2-binary


urllib.request error -->
Once upon a time I stumbled with this issue. If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file. :D


Properties

f1650f2a99824f349643ad234abff6a2
{-73.7491701543331,40.9182316369111,-73.748331964016,40.9188650080518}
43 Magnolia Avenue, Larchmont, NY 10538

f853874999424ad2a5b6f37af6b56610
{-80.0827648490667,26.3244657485548,-80.0819266587496,26.3252170139397}
Boca Raton

3290ec7dd190478aab124f6f2f32bdd7
{-80.0786402821541,26.8845993458896,-80.0778020918369,26.8853469410407}

5e25c841f0ca47ac8215b5fd0076259a
{-87.6440555602312,41.9226562956759,-87.6432173699141,41.9232799459277}
Lincoln Park chicago

622088210a6f43fca2a1824e8610df03
{-80.0741911679506,26.3864299315496,-80.0733529776335,26.3871807943469}



pip install -r requirements.txt


To build docker image

`docker build -t zesty .`


docker login
docker tag f7fb4bb76b9d suejungshin/zesty-app:latest  (that is the docker image name)
docker push suejungshin/zesty-app:latest

    volumes:
      - ./wait-for-it.sh:/usr/local/bin/wait-for-it.sh
    command:
      - wait-for-it.sh
      - postgres:5432
      - --
      - python3
      - index.py


To run tests:
docker exec -it af6cad9cf311 pytest

To enter container:
docker exec -it af6cad9cf311 bash
ctrl + d to exit