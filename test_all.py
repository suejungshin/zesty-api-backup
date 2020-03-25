import pytest
import urllib.request
import io
import json
import ast
from pathlib import Path

import models
import controllers

path = Path.cwd()
url = "http://localhost:8080"
# to run, navigate to folder,  "pytest"  (& make sure server is running first)

def test_is_server_running():
    try:
        urllib.request.urlopen(url)
        assert True
    except:
        assert False

def test_get_image_url():
    actual = models.get_image_url("f1650f2a99824f349643ad234abff6a2")
    expected = "https://storage.googleapis.com/engineering-test/images/f1650f2a99824f349643ad234abff6a2.tif"

    assert expected == actual

def test_get_image():
    endpoint = "/api/display/"
    id_OK = "f853874999424ad2a5b6f37af6b56610"

    response1 = io.BytesIO(urllib.request.urlopen(url + endpoint + id_OK).read())
    assert response1

    image_path_1 = f"{path}/images/{id_OK}.jpeg"
    assert Path(image_path_1).exists() == True

    try:
        id_err = "25"
        urllib.request.urlopen(url + endpoint + id_err).read()
    except urllib.error.HTTPError as e:
        assert e.code == 404

    image_path_2 = f"{path}/images/{id_err}.jpeg"
    assert Path(image_path_2).exists() == False

def test_get_image_overlayed():

    overlayed = "?overlayed=true"
    endpoint = "/api/display/"
    id_OK = "f853874999424ad2a5b6f37af6b56610"

    response1 = io.BytesIO(urllib.request.urlopen(url + endpoint + id_OK + overlayed).read())
    assert response1

    image_path_1 = f"{path}/images/{id_OK}-overlayed.jpeg"
    assert Path(image_path_1).exists() == True

    try:
        id_err = "25"
        urllib.request.urlopen(url + endpoint + id_err + overlayed).read()
    except urllib.error.HTTPError as e:
        assert e.code == 404

    image_path_2 = f"{path}/images/{id_err}-overlayed.jpeg"
    assert Path(image_path_2).exists() == False


def test_get_nearby_properties():
    endpoint = "/api/find"

    values1 = json.dumps({
        "type": "Feature",
        "geometry": {
        "type": "Point",
        "coordinates": [-80, 26]
    },
        "distance_meters": 100000000
    })

    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    req1 = urllib.request.Request(url + endpoint, values1.encode(), headers)
    response1 = urllib.request.urlopen(req1).read()
    result_list1 = ast.literal_eval(response1.decode())
    assert len(result_list1) == 5

    values2 = json.dumps({
        "type": "Feature",
        "geometry": {
        "type": "Point",
        "coordinates": [-80, 26]
    },
        "distance_meters": 1
    })
    req2 = urllib.request.Request(url + endpoint, values2.encode(), headers)
    response2 = urllib.request.urlopen(req2).read()
    result_list2 = ast.literal_eval(response2.decode())
    assert len(result_list2) == 0

def test_get_total_parcels_area():
    id1 = "622088210a6f43fca2a1824e8610df03"
    id2 = "f1650f2a99824f349643ad234abff6a2"
    radius1 = 100
    radius2 = 1000000

    assert models.get_total_parcels_area(id1, radius1) == 2330.55982263293
    assert models.get_total_parcels_area(id1, radius2) == 6083.88748867391

    assert models.get_total_parcels_area(id2, 0) == 911.830634661019
    assert models.get_total_parcels_area(id2, radius2) == 911.830634661019

def test_get_nearby_buildings_details():
    id = "622088210a6f43fca2a1824e8610df03"
    radius1 = 100
    radius2 = 1000000
    expected1 = [[981.199068874121], [0.0]]
    expected2 = [[728.408156002639, 755.948145020753, 981.199068874121], [6903.42435103, 55182.24068712, 0.0]]

    # pytest tests for deep equality
    assert models.get_nearby_buildings_details(id, radius1) == expected1
    assert models.get_nearby_buildings_details(id, radius2) == expected2

def test_get_zone_density():
    id = "622088210a6f43fca2a1824e8610df03"
    radius1 = 100
    radius2 = 0
    radius3 = 10000000 # At distance = 10000000 meters, the ST_Buffer and ST_Intersection seem to break down

    assert models.get_zone_density(id, radius1) == 3.1415629859896486
    assert models.get_zone_density(id, radius2) == 100
    assert models.get_zone_density(id, radius3) == None
