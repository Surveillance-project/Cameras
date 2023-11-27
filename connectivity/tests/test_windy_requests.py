from unittest.case import TestCase as UnitCase
from services.connectivity import WindyApi, WebcamLifecyclePeriod


class AuthorizesTest(UnitCase):
    def setUp(self):
        self.api = WindyApi()

    def test_authorization(self):
        self.api.authorize()


class GetWebcamSchemeTest(UnitCase):
    def setUp(self):
        self.webcam_id = 1179853135
        self.api = WindyApi()

    def test_get_full_scheme(self):
        self.api.get_camera(self.webcam_id)


class GetPlayerUrlTest(UnitCase):

    def setUp(self):
        self.api = WindyApi()
        self.webcam_scheme = {
            "title": "Sydney: Sydney Harbour Bridge - Sydney Opera House",
            "viewCount": 1387607,
            "webcamId": 1179853135,
            "status": "active",
            "lastUpdatedOn": "2023-11-26T13:29:36.000Z",
            "player": {
                "live": "https://webcams.windy.com/webcams/public/embed/player/1179853135/live",
                "day": "https://webcams.windy.com/webcams/public/embed/player/1179853135/day",
                "month": "https://webcams.windy.com/webcams/public/embed/player/1179853135/month",
                "year": "https://webcams.windy.com/webcams/public/embed/player/1179853135/year",
                "lifetime": "https://webcams.windy.com/webcams/public/embed/player/1179853135/lifetime"
            }
        }

    def test_get_player_for_day_url(self):
        self.api.get_player_url(self.webcam_scheme)

    def test_get_player_for_live_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.LIVE)

    def test_get_player_for_month_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.MONTH)

    def test_get_player_for_year_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.YEAR)


class GetPlayerHTMLTest(UnitCase):

    def setUp(self):
        self.api = WindyApi()
        self.player_for_day_url = "https://webcams.windy.com/webcams/public/embed/player/1179853135/day"

    def test_return_html(self):
        html_string = self.api.get_player_html(self.player_for_day_url)
        self.assertTrue(html_string.strip().strip('\n').startswith("<!doctype html>"))


class GetPlayerImagesUrlsTest(UnitCase):
    def setUp(self):
        self.api = WindyApi()
        self.html = '''
        

<!doctype html>
<html>

<head>
	<title>Windy.com Player embed</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta id="viewport" name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
    <script>
		var WindyPlayer = {
			archiveType: 'day',
			autoPlay: false,
			forceFullScreenOnOverlayPlay: false,
			interactive: true,
			loop: false,
			speed: 1.25,
			pause: 0.25,
			imageExpireTimestamp: 1701015519119,
			times: ['Sun 02:50','Sun 03:50','Sun 04:51','Sun 05:49','Sun 06:46','Sun 07:45','Sun 08:43','Sun 09:57','Sun 10:55','Sun 11:53','Sun 12:50','Sun 14:03','Sun 15:16','Sun 16:11','Sun 17:07','Sun 18:05','Sun 19:04','Sun 20:06','Sun 21:08','Sun 22:08','Sun 23:10','Mon 00:08','Mon 01:07','Mon 02:07','Mon 02:49'],
			slides: {
				preview: ['https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700927448.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTI3NDQ4LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.i8PnU_qT8bCMfCnmoVc9b8rL6x7sofRowyofppJcviM','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700931018.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTMxMDE4LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.47YBhhNHWBIEiNcIcRmxTlf-gXxAUV_lWc3rMJ7E6FQ','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700934689.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTM0Njg5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.8X9imXldmt4k_THLoAIYhNlJtV4SDBo4iUUi7k0SKdM','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700938183.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTM4MTgzLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.vWuQL2b13CNetH-1Cbyh9yqybJw7XxKJpxZuFr8wHgo','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700941619.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTQxNjE5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.LrnA776s3_pPlE-dLaU5VNqSNQmH2TQ08THHx0FgtkA','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700945147.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTQ1MTQ3LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.yVopXy2PhByMB8D_RrWHEHrl4HUJ--IbXnhE_6H1x0A','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700948632.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTQ4NjMyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.27aQjLs_SFAL_Sb_d3KTdcPoN0t0X8t2K5z8VlLh2wQ','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700953056.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTUzMDU2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.ZQKqfYRXXNAFcVso1lkpp-Qb6FJrNxCmivl88_Fe8-c','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700956505.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTU2NTA1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.YGy-0VG0Kc3U-E1EwaewVgt8uM2HiI9YUCZqvqGvZHY','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700959981.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTU5OTgxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.4Z6s8ptf1fMQE9rHrIymQ4c1a-_ZyMGxmP112aCzzHM','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700963436.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTYzNDM2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.8uazmK3nwAWfmxe6kD9sYpjyWY_dyy4FGuggKecNuvw','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700967789.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTY3Nzg5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.jWh3FVo1SqRx3Nrd1lNWv6K9hf7odKe1IzaJHZmOY64','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700972172.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTcyMTcyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.5c_fsu1roaq8YWbatJw-UDNljiR0E_YA1SSAsFDt0UA','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700975506.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTc1NTA2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.vIiOxvgq67aIlFQrh1afbpOaXlcTFFwsjRWEKPh6rXU','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700978835.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTc4ODM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.pk_fn-0-1pUleTUhi0TGGYuk11WTllcM4QdyJ0IcjlY','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700982317.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTgyMzE3LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.RWI6uYYiouXC13TAd8FNZGps3aaiDXiWwbxR4Qc-JOw','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700985861.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTg1ODYxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.6oMA510u0-yVM8BnZPg8G_lRqaP5QdQusb-bGV_SzGk','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700989562.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTg5NTYyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.FHRluzc0pCF51trs2aro1ajyHhiuaMNJeDyc79Q7QsU','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700993302.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTkzMzAyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.DwFxjX_4_rCZWYCoTimXMBrFVK7noIEQCJdSwy711HE','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1700996919.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAwOTk2OTE5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.U5BRBlvqTAGqow0ksYAPmWxUi6-2IH6JDHBrJJhiylI','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1701000635.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAxMDAwNjM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.Q9XvzZHPyuE3zfBxN4HjmiNg9UIh0WRRVfi7cJmmHE4','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1701004103.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAxMDA0MTAzLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.Ws-fiHQuR7L5hOhnsWGZbo4CrLFw0e1eH36TZoAp-So','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1701007665.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAxMDA3NjY1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.0OjAmVob9YM616xyFKdqh3R61GmpuLJ4OYOJJaVPQg4','https://images-webcams.windy.com/public/archive/35/1179853135/day/preview/1179853135@1701011261.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L3ByZXZpZXcvMTE3OTg1MzEzNUAxNzAxMDExMjYxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.MHCY4B_iHQ4xRsjVjdpeIha1yOJuYlyiGLYCxLL1WSs','https://images-webcams.windy.com/public/35/1179853135/current/preview/1179853135.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy8zNS8xMTc5ODUzMTM1L2N1cnJlbnQvcHJldmlldy8xMTc5ODUzMTM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMDE1NTQ5fQ.bDzewaG3P6os2b3bCOI88t7FlcHU1askBaH_iQCoFCw'],
				normal: ['https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700927448.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5Mjc0NDguanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.th5kv4ireThvtC5hZ2RAhuF8Dj6UoGOTVAXu-S6lUMQ','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700931018.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5MzEwMTguanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.RUU25ArOb711NZoc-ecjlEMtG3dTk3toa8v3kRGZzFc','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700934689.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5MzQ2ODkuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.XdOP6K85B5H_5s7wPbkgOFXBDiaDuGAKHmZWr9zOsIQ','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700938183.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5MzgxODMuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.1RmD_FcfyIDqZ7PT84x1HDz2U8zPPR8JeuJ0BwDtyew','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700941619.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NDE2MTkuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.cHlUmG7UAwF4yZx4oi8zg5FsvP4E-SzXBVVuy1yMcOQ','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700945147.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NDUxNDcuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.hfaP2KfYxTgmp3I9WV2FhnJ2fCYEJ6O_EmTGhtTqrYw','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700948632.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NDg2MzIuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.R9VpQ6EygbkUrMLenyKXI2jErw9LxMKeKFEB06W8sus','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700953056.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NTMwNTYuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.tjADI3gHrPLpD9OD9da3KOn-0QxYIpqLp-P_iB0xrh0','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700956505.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NTY1MDUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9._V36bNMWz3JUUXdBUJ-ZOZcB9iz8LBB7UuTZnPv_ScM','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700959981.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NTk5ODEuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.HM5-WG1OFATFi0Hj-LTYNoku7Q4i929E-UB0Iva-GGs','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700963436.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NjM0MzYuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.HeTLFG4BHHv2CMTnb1xqGW2CifzADAdOqc2wIFCIxSU','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700967789.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5Njc3ODkuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.N_SAdsCril0doctcVySLS7Yk3LIY0C4h4_8IFL6eDqs','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700972172.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NzIxNzIuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.lPjR4zNUrWF-CPxpPRPa1GQYiy-5Ej66SAMjUrygqRk','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700975506.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5NzU1MDYuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.idJs4c_TezyHcYjnRwy2d7rO65ptfapTUM_qfgjLBbU','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700978835.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5Nzg4MzUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.WyZGTmbl4RS4-l_OHzAOTNTCMHyRFNme-yCyehn6Qds','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700982317.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5ODIzMTcuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.9M7J0VQEYWtOeEs74866dTnPmzKaNnEEXjQFTttJ6j8','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700985861.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5ODU4NjEuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.FYSoH-k4R35DWbETyG7RvUFb3TU0UIvuGwiMJXzytBo','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700989562.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5ODk1NjIuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.4NTD47HmCt1gdMfRkIga-DX8k38LNFNzCbV7_queDAc','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700993302.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5OTMzMDIuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.PwCeb38XFfHqVPXDLnQkhguLksLK-o31qvohP3DtFQ0','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1700996919.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDA5OTY5MTkuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.2zFk0m2swXJ0wwBeSGyZAxye7UCMmlHmTvpjsQas6n8','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1701000635.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDEwMDA2MzUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.ksBncSagX_zBVYrtnHuXaHjNfDPtkYtA37W1LogO0H0','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1701004103.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDEwMDQxMDMuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.3_Qb7GUV7vJo9jREu9r4MgP_iLIRL-I5xs4_bzM6OP8','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1701007665.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDEwMDc2NjUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.XolZsaGiXa7sU9eXhbWuPtf1tZkZtQBK95HIK1xmoy4','https://images-webcams.windy.com/public/archive/35/1179853135/day/normal/1179853135@1701011261.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L25vcm1hbC8xMTc5ODUzMTM1QDE3MDEwMTEyNjEuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDExMDEzNDl9.T0rCcE-7Arv8_CkFzQ8uOlDaMd5h7UK_sMt3WBiI7T8','https://images-webcams.windy.com/public/35/1179853135/current/normal/1179853135.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy8zNS8xMTc5ODUzMTM1L2N1cnJlbnQvbm9ybWFsLzExNzk4NTMxMzUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDEwMTU1NDl9.nMOiXoXBm0JdquQoBxtoEmaEE_SBf51HrHU0GlbsKYw'],
				full: ['https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700927448.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTI3NDQ4LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.GRgQwoA_RbGNu9wE9QC32kALsdOig5roe1eoLlHY_7U','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700931018.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTMxMDE4LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.gBckyG4C2rnQ0SubEiGTuZXCqck-R9Nj6hdY53x2i40','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700934689.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTM0Njg5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.ejYGzDWuXIs5NVMla2k1JIbHCj8LJ9UYvPk7z_gmi2w','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700938183.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTM4MTgzLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.PxcR85IM_dz-Q80-Z5qOI3KoFqAZdqQTV3DjWkpk5AU','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700941619.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTQxNjE5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.yvQUU1pVM8_nozfcJuAaVN9ZwpXPNss-M2c4cLz47H4','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700945147.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTQ1MTQ3LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.SoT-IZKqD5yh3z-kep3LpW3jMEz_wwrtuYzLFbEUvbU','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700948632.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTQ4NjMyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.RvButSJF8oUh8vRiNiAghfe04xBg-22MeF8dp8UioFw','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700953056.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTUzMDU2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.Ok5hR8XWqKJuOtXlflQfJA3a1Ad937deccNdhZ8JuBA','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700956505.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTU2NTA1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.cCRpB6jhu-Ng-9ycA1CEsjt0USCiECHfKVcEYsCQdyw','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700959981.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTU5OTgxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.15ghoMJIb805X_djgs_LXzvxk915oq4p61KiYVqgFno','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700963436.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTYzNDM2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.7ZSrKJ5rSrERhf9bD81LfgWkI4HzF4JUi8hhRzAjDms','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700967789.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTY3Nzg5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.lp3S2u8toa2Pt0P02HVv0zQYPdjnAu_GDAZfbq1l8zU','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700972172.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTcyMTcyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.yMU4rHjdeaGODNyLaHwJ-0mpKrnOrT68piAaOkpXYTM','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700975506.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTc1NTA2LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.8_smuLTftXKPK_dpn0wfQxi1PhIbQkzqs5uDIByqHaw','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700978835.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTc4ODM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.HcYeNeEmuxvHNHSC_PeUl9tNep_IQ3auUZ83Jo6bGHo','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700982317.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTgyMzE3LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.pUcZqtxu0tT7sg7G7JlTw3NGP19peATUnYtJDafFrTU','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700985861.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTg1ODYxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.YH7erw_OiWGDvrtjXgiPzWmrdOCKMBpTE6Op_kcCpjg','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700989562.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTg5NTYyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.RBgRz_68VzV4dMYPiyjRzqeUDYWMTOxev23sIrdhAgU','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700993302.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTkzMzAyLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.uBCacDMfQXgrd2XzUnO-65TNlsLtzP-4u7bkVQLV9bY','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1700996919.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAwOTk2OTE5LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.iubfD3Lyr7HnuI-JjvPn3L_EOngEnwcDJJF0Uy8-Pug','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1701000635.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAxMDAwNjM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.kSvxOAAvDaMXtq6qCWY0pyCWN25jpoZR-H8EpJ2EWcc','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1701004103.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAxMDA0MTAzLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.H0VoY0oaRwhvrjxhhrcblXqFzGiLY16uJ2DtVE1k9K0','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1701007665.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAxMDA3NjY1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.xZ-QFuE4fhYHecruPmSqx-wlgTOcXN43HoKQsT8RzPY','https://images-webcams.windy.com/public/archive/35/1179853135/day/full/1179853135@1701011261.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy9hcmNoaXZlLzM1LzExNzk4NTMxMzUvZGF5L2Z1bGwvMTE3OTg1MzEzNUAxNzAxMDExMjYxLmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMTAxMzQ5fQ.70R_gFUFLGPGhlVKU6raOc2ZgjHWz560MCA-XNEzrU8','https://images-webcams.windy.com/public/35/1179853135/current/full/1179853135.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy8zNS8xMTc5ODUzMTM1L2N1cnJlbnQvZnVsbC8xMTc5ODUzMTM1LmpwZyIsImlhdCI6MTcwMTAxNDk0OSwiZXhwIjoxNzAxMDE1NTQ5fQ.C8qNORx8N14HyR3IuKfrO5wWQoxMIet8N8C7xNwX5-0'],
			},
			teaserbg: 'https://images-webcams.windy.com/public/35/1179853135/current/teaserbg/1179853135.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy8zNS8xMTc5ODUzMTM1L2N1cnJlbnQvdGVhc2VyYmcvMTE3OTg1MzEzNS5qcGciLCJpYXQiOjE3MDEwMTQ5NDksImV4cCI6MTcwMTAxNTU0OX0.Snrwla7YvDXfcXlZBY2iwNLvDum8y4phrEj4-q6yix4',
			device: 'desktop',
		}
    </script>

	<link rel="canonical" href="https://windy.com/webcams/1179853135">
	<link rel="stylesheet" type="text/css" href="/webcams/public/embed/v2/style/player.css">
</head>

<body id="body" class="desktop">
	<noscript>
		<div class="warning">JavaScript needed</div>
	</noscript>
	<div id="warningScreenTooSmall" class="warning" style="display:none">
		Area too small<br>
		<small>Required: 200x110px</small>
	</div>

	<div id="wrapper">
		<div id="content">
			<div id="infoBox" class="overlayBox">
				<div class="left">
					<div>Source: <a href="https://webcamsydney.com/" target="_blank">https://webcamsydney.com/</a></div>
					<div>For developers: <a href="https://api.windy.com/webcams" target="_blank" id="info-problem">Windy API</a></div>
				</div>
				<dvi class = "right">
					<a href="https://windy.com/webcams/edit/1179853135" id="feedback" class="edit-icon icon" target="_blank">Give feedback</a>
					<a href="https://www.windy.com/webcams/add" id="info-add" class="webcam-icon icon" target="_blank">Add a webcam</a>
				</div>
			</div>
			<div id="mainOverlay"></div>
			<div id="webcam" data-image-dimensions='{ "width": 1920, "height": 1080 }'>
				<a id="overlayPlay" >
					<span id="overlayPlayIcon" class="play-icon icon"></span>
				</a>
				<a id="overlayPause" class="minimized-before">
					<span id="overlayPauseIcon" class="pause-icon icon"></span>
				</a>
				<a id="overlayLoading" style="display:none"></a>
				<a id="slideshow" class="slides">
					<img id="background" src="https://images-webcams.windy.com/public/35/1179853135/current/normal/1179853135.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZV9wYXRoIjoiL3B1YmxpYy8zNS8xMTc5ODUzMTM1L2N1cnJlbnQvbm9ybWFsLzExNzk4NTMxMzUuanBnIiwiaWF0IjoxNzAxMDE0OTQ5LCJleHAiOjE3MDEwMTU1NDl9.nMOiXoXBm0JdquQoBxtoEmaEE_SBf51HrHU0GlbsKYw">
				</a>
				<div style="display:none;">
					<img id="coverTemplate" class="cover">
				</div>
			</div>
			<div id="player">
					<div id="progress">
						<div id="progressBar"> </div>
						<div id="progressTooltip">
							0 / 
						</div>
						<span id="pointer"/>
					</div>
				<div id="controls-part">
					<div>
						<a id="play" class="play-icon icon"  ></a>
						<span id="pause" class="pause-icon icon"></span>
					</div>
					<div id="controls-right">
							<span id="time" class="text nobreak">
								Mon 02:49
							</span>
						<div id="timelapses-wrapper">
							<span id="timelapses" class="dropdown-icon timelapses-icon">
								24 hours
							</span>
								<div id="timelapsesBox">
											<a href="/webcams/public/embed/player?archiveType&#x3D;month&amp;webcamId&#x3D;1179853135&amp;loop&#x3D;0&amp;interactive&#x3D;1&amp;forceFullScreenOnOverlayPlay&#x3D;0&amp;referrer&#x3D;https%3A%2F%2Fwebcams.windy.com%2Fwebcams%2Fpublic%2Fembed%2Fplayer%2F1179853135%2Flive&amp;sr&#x3D;undefined" class="timelapse-link" >
												<div><span>30 days</span></div>
											</a>
											<a href="/webcams/public/embed/player?archiveType&#x3D;year&amp;webcamId&#x3D;1179853135&amp;loop&#x3D;0&amp;interactive&#x3D;1&amp;forceFullScreenOnOverlayPlay&#x3D;0&amp;referrer&#x3D;https%3A%2F%2Fwebcams.windy.com%2Fwebcams%2Fpublic%2Fembed%2Fplayer%2F1179853135%2Flive&amp;sr&#x3D;undefined" class="timelapse-link" >
												<div><span>12 months</span></div>
											</a>
											<a href="/webcams/public/embed/player?archiveType&#x3D;lifetime&amp;webcamId&#x3D;1179853135&amp;loop&#x3D;0&amp;interactive&#x3D;1&amp;forceFullScreenOnOverlayPlay&#x3D;0&amp;referrer&#x3D;https%3A%2F%2Fwebcams.windy.com%2Fwebcams%2Fpublic%2Fembed%2Fplayer%2F1179853135%2Flive&amp;sr&#x3D;undefined" class="timelapse-link" >
												<div><span>Lifetime</span></div>
											</a>
											<a href="https://webcams.windy.com/webcams/stream/1179853135" class="timelapse-link" target='_blank'>
												<div><span>Live stream</span></div>
											</a>
								</div>
						</div>
						<a id="info" class="info-icon icon"></a>
						<div>
							<a id="fullscreen-enter" class="fullscreen-enter-icon icon " href="/webcams/public/embed/player?archiveType&#x3D;day&amp;webcamId&#x3D;1179853135&amp;loop&#x3D;0&amp;interactive&#x3D;1&amp;forceFullScreenOnOverlayPlay&#x3D;0&amp;referrer&#x3D;https%3A%2F%2Fwebcams.windy.com%2Fwebcams%2Fpublic%2Fembed%2Fplayer%2F1179853135%2Flive&amp;sr&#x3D;undefined" target="_blank"></a>
							<a id="fullscreen-exit" class="fullscreen-exit-icon icon " target="_blank"></a>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>

<script src="/webcams/public/embed/v2/script/player/screenfull.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/x-browser.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/dom.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/shared.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/overlays.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/progress-bar.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/full-screen.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/image.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/player.js" onpublish="merge"></script>
<script src="/webcams/public/embed/v2/script/player/responsible.js" onpublish="merge"></script>

</html>


        '''

    def test_get_images_urls(self):
        urls = self.api.get_player_images_urls(self.html)
        self.assertIsInstance(urls, list)


class GetImagesPipelineTest(UnitCase):
    def setUp(self):
        self.webcam_id = 1179853135
        self.api = WindyApi()

    def test_download_images(self):
        images = self.api.get_images(self.webcam_id, WebcamLifecyclePeriod.DAY)
        self.assertIsNot(bool(images), False)
