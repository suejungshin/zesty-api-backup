import web
import geojson
import json
import controllers
import models

web.config.debug = False

urls = (
    "/api/display/(.*)", "Display",
    "/api/find", "Find",
    "/api/statistics/(.*)", "Statistics",
    "/api/analyze", "Analyze",
    "/", "Home"
)

class Display:
    def GET(self, id):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Credentials", "true")
        web.header('Content-Type', 'image/jpeg')

        try:
            data = web.input()
            overlay = json.loads(data.overlayed.lower())
        except:
            overlay = False

        image = controllers.get_image(id, overlay)

        if not image:
            return app.notfound()
        else:
            return image

class Find:
    def POST(self):
        data = web.data()
        geojson_obj = geojson.loads(data)

        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Credentials", "true")
        web.header("Content-Type", "application/json")

        return controllers.get_nearby_properties(geojson_obj)

class Statistics:
    def GET(self, id):
        data = web.input()
        distance = data.distance

        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Credentials", "true")
        web.header("Content-Type", "application/json")

        return controllers.get_stats(id, distance)


class Home:
    def GET(self):
        return "API service for properties information"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()