from django.shortcuts import render
from urllib.request import urlopen
# Create your views here.
# (Brains behind the scene with python.
# Use python to reflect in our APP/WebPage)


def home(request):
    """POST and GET requests (Brush up on HTML5 and CSS Forms)"""
    if request.method == "POST":
        city = request.POST['citylookup']
        city, country, localtime, date = get_weatherInfo(request, city)
        return jumbotron(request, city, country, localtime, date)

    else:
        """On GET request, get the visitor's local city's Air Quality"""
        ip = get_ip(request)
        city = urlopen(f"https://ipapi.co/{ip}/city").read().decode("utf-8")
        city, country, localtime, date = get_weatherInfo(request, city)
        return jumbotron(request, city, country, localtime, date)


def get_ip(request):
    """Get visitor's IP from scraping a certain website"""
    url = "".join(
        urlopen('https://ipapi.co').read().decode("utf-8")[3890:3965].split())
    begin = url.find('<h1>') + 4
    end = url.find('</h1>')
    ip = url[begin:end]
    return ip


def get_weatherInfo(requests, city):
    """Get weatherInfo from an other API"""
    import requests
    import datetime

    try:
        api_json2 = requests.get(
            "http://api.weatherstack.com/current?access_key=f4ec8c3283872a7de69e9ec1129bfebf&query=" + city).json()
        city = api_json2['location']['name']
        country = api_json2['location']['country']
        localtime = api_json2['location']['localtime'].split()[1]
        date = api_json2['location']['localtime'].split()[0]

        return city, country, localtime, date

    except Exception as e:
        return city, city, city, city


def jumbotron(request, city, country, localtime, date):
    """Jumbotron"""
    import requests

    try:
        api_json = requests.get(
            "https://api.waqi.info/feed/" + city + "/?token=d4d75f4262bb8bf35993a20496b828b963580311").json()

        try:
            # Create special error Jumbotron
            if api_json['status'] == 'error':
                aqi = "Error"
                category_color = "error"
                status_description = "No data seems to be available for {}.".format(
                    city)
                raise Exception
            else:
                # Gets Air Quality value from JSON file.
                aqi = api_json['data']['aqi']
                category_color = ''

                # Alter state of Jumotron
                if aqi <= 50:
                    aqi = "Good"
                    category_color = "good"
                    status_description = "(0 - 50) - Air quality is considered satisfactory, and air pollution poses little or no risk"
                elif 51 <= aqi <= 100:
                    aqi = "Moderate"
                    category_color = "moderate"
                    status_description = "(51 - 100) - Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
                elif 101 <= aqi <= 150:
                    aqi = "Unhealthy for Sensitive Groups"
                    category_color = "usg"
                    status_description = "(101 - 150) - Members of sensitive groups may experience health effects. The general public is not likely to be affected."
                elif 151 <= aqi <= 200:
                    aqi = "Unhealthy"
                    category_color = "unhealthy"
                    status_description = "(151 - 200) - Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
                elif 201 <= aqi <= 300:
                    aqi = "Very Unhealthy"
                    category_color = "veryunhealthy"
                    status_description = "(201 - 300) - Health warnings of emergency conditions. The entire population is more likely to be affected."
                elif aqi > 300:
                    aqi = "Hazardous"
                    category_color = "hazardous"
                    status_description = "(300+) - Health alert: everyone may experience more serious health effects!!"

        except Exception as e:
            aqi = "An error as occurred!"

    except Exception as e:
        api_json = "Error with API..."

    return render(request, 'home.html', {'api_json': api_json,
                                         'aqi': aqi, "category_color": category_color,
                                         "status_description": status_description,
                                         "city": city, "country": country,
                                         "localtime": localtime, "date": date
                                         })
