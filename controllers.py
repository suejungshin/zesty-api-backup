import models
import io
import geojson
import json
import urllib.request
from PIL import Image, ImageDraw
from pathlib import Path

path = Path.cwd()

def translate_coords(arr, bounds, size):
    lon0 = bounds[0]
    lat0 = bounds[1]
    lon_scale = size[0] / (bounds[2] - bounds[0])
    lat_scale = size[1] / (bounds[3] - bounds[1])
    res = []
    for coord in arr:
        lon = coord[0]
        lat = coord[1]
        res.append(((lon - lon0) * lon_scale, size[1] - (lat - lat0) * lat_scale))
    return res

def draw_overlay(id):
    result = models.get_property_details(id)
    bldg_latlongs = geojson.loads(result[0]).coordinates[0]
    parcel_latlongs = geojson.loads(result[1]).coordinates[0]
    image_bounds = result[2]

    im = Image.open(f"./images/{id}.jpeg")
    size = im.size
    parcel_pxls = translate_coords(parcel_latlongs, image_bounds, size)
    bldg_pxls = translate_coords(bldg_latlongs, image_bounds, size)

    polyg = Image.new('RGBA', size)
    pdraw = ImageDraw.Draw(polyg)
    pdraw.polygon(parcel_pxls, fill=(255,255,0,128))
    pdraw.polygon(bldg_pxls, fill=(255,0,0,128))
    im.paste(polyg, mask=polyg)
    image_path = f"{path}/images/{id}-overlayed.jpeg"
    im.save(image_path, format="JPEG")
    return

def save_image_from_url(id):
    image_url = models.get_image_url(id)

    if image_url is None:
        return False

    bytes_obj = urllib.request.urlopen(image_url).read()
    image = Image.open(io.BytesIO(bytes_obj))

    image_path = f"{path}/images/{id}.jpeg"
    image.save(image_path, format="JPEG")
    return True

def get_image(id, overlay):

    if overlay:
        image_path = f"{path}/images/{id}-overlayed.jpeg"
    else:
        image_path = f"{path}/images/{id}.jpeg"

    try:
        return open(image_path, "rb")
    except FileNotFoundError:
        success = save_image_from_url(id)
        if not success:
            return None
        else:
            if overlay:
                draw_overlay(id)
                return open(image_path, "rb")
            else:
                return open(image_path, "rb")

def get_nearby_properties(geojson_obj):
    return models.find_nearby_property_ids(geojson_obj)

def get_stats(id, distance):
    total_parcel_area_in_radius = models.get_total_parcels_area(id, distance)
    buildings_detail = models.get_nearby_buildings_details(id, distance)
    areas = buildings_detail[0]
    distances = buildings_detail[1]
    zone_density = models.get_zone_density(id, distance)

    if not zone_density:
        zone_density = "Search distance was too large"

    return json.dumps({
        "total_parcel_area_in_radius": total_parcel_area_in_radius,
        "buildings_areas": areas,
        "buildings_dists_to_center": distances,
        "zone_density": zone_density
    })