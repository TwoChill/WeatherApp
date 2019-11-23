from django.shortcuts import render
from urllib.request import urlopen
# Create your views here.
# (Brains behind the scene with python.
# Use python to reflect in our APP/WebPage)


def get_ip(request):
    """Get visitor's IP from scraping a website"""
    url = "".join(urlopen('https://ipapi.co').read().decode("utf-8")[3890:3965].split())
    begin = url.find('h1>') + 3
    end = url.find('</h1>')
    ip = url[begin:end]
    return ip


def home(request):
    """POST and GET requests (Brush up on HTML5 and CSS Forms)"""
    if request.method == "POST":
        city = request.POST['citylookup']
        return jumbotron(request, city)

    else:
        ip = get_ip(request)
        city = urlopen(f"https://ipapi.co/{ip}/city").read().decode("utf-8")
        return jumbotron(request, city)


def aboutme(request):
    """About Me Page"""
    return render(request, 'aboutme.html', {})


def jumbotron(request, city):
    """Jumbotron"""
    import requests

    try:
        api_json = requests.get("https://api.waqi.info/feed/" + city + "/?token=d4d75f4262bb8bf35993a20496b828b963580311").json()

        try:
            if api_json['status'] == 'error':
                aqi = "Error"
                category_color = "error"
                status_description = "No data seems to be available for {}.".format(city)
                raise Exception
            else:
                # Gets Air Quality value from JSON file.
                aqi = api_json['data']['aqi']
                category_color = ''

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

    return render(request, 'home.html', {'api_json': api_json, 'aqi': aqi, "category_color": category_color, "status_description": status_description})
