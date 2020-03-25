from psycopg2 import connect
import json
import os

host = os.environ.get("POSTGRES_HOST", "localhost")
port = os.environ.get("POSTGRES_PORT", "5555")

conn = connect(
    dbname = "zesty",
    user = "postgres",
    password = "engineTest888",
    host = host,
    port = int(port)
)

cursor = conn.cursor()

def get_image_url(id):
    SQL = "SELECT image_url FROM properties WHERE id=%s;"
    data = [id]
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()

        if result is None:
            return None
        else:
            return result[0]
    except:
        conn.rollback()
        return None


def get_property_details(id):
    SQL = "SELECT ST_AsGeoJSON(building_geo), ST_AsGeoJSON(parcel_geo), image_bounds FROM properties WHERE id=%s;"
    data = [id]
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result
    except:
        conn.rollback()
        return None


def find_nearby_property_ids(geojson_obj):
    distance = geojson_obj.distance_meters
    geom = json.dumps(geojson_obj.geometry) # ST_GeomFromGeoJSON requires type to be "str" intsead of "geojson.feature", so convert to json

    SQL = """SELECT id
            FROM properties
            WHERE ST_DWithin( geocode_geo , ST_GeomFromGeoJSON(%s), %s )"""
    data = [geom, distance]
    try:
        cursor.execute(SQL, data)
        tuples = cursor.fetchall()
        return [tuple[0] for tuple in tuples]
    except:
        conn.rollback()
        return None

def get_total_parcels_area(id, radius):
    SQL = """SELECT sum(ST_Area(parcel_geo))
            FROM properties
            WHERE ST_DWithin( geocode_geo,
                    (SELECT geocode_geo FROM properties WHERE id=%s),
                    %s )"""
    data = [id, radius]
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()

        if result is None:
            return None
        else:
            return result[0]
    except:
        conn.rollback()
        return None

def get_nearby_buildings_details(id, distance):
    SQL = """SELECT ST_Area(building_geo),
                    ST_Distance(building_geo, (SELECT geocode_geo FROM properties WHERE id=%s))
            FROM properties
            WHERE ST_DWithin( geocode_geo,
                              (SELECT geocode_geo FROM properties WHERE id=%s),
                              %s )"""
    data = [id, id, distance]
    try:
        cursor.execute(SQL, data)
        tuples = cursor.fetchall()
        areas = []
        distances = []
        for tuple in tuples:
            areas.append(tuple[0])
            distances.append(tuple[1])
        return [areas, distances]
    except:
        conn.rollback()
        return None

def get_zone_density(id, distance):
    SQL = """SELECT SUM(
                        ST_Area(
                            ST_Intersection(
                                building_geo,
                                ST_Buffer( (SELECT geocode_geo FROM properties WHERE id=%s),
                                            %s
                                )
                            )
                        )
                    ),
                    ST_Area(
                        ST_Buffer( (SELECT geocode_geo FROM properties WHERE id=%s),
                                    %s
                        )
                    )
            FROM properties"""
    data = [id, distance, id, distance]
    try:
        cursor.execute(SQL, data)
        result = cursor.fetchone()
        if result[1] == 0:
            return 100
        else:
            return result[0] / result[1] * 100
    except:
        conn.rollback()
        return None