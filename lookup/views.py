from django.shortcuts import render
from urllib.request import urlopen
# Create your views here.
# (Brains behind the scene with python.
# Use python to reflect in our APP/WebPage)


def home(request):
    """POST and GET requests (Brush up on HTML5 and CSS Forms)"""
    page = 'home'

    if request.method == "POST":
        city = request.POST['citylookup']
        city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir = get_weatherInfo(
            request, city)
        return jumbotron(request, page, city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir)

    else:
        """On GET request, get the visitor's local city's Air Quality"""
        ip = get_ip(request)
        city = urlopen(f"https://ipapi.co/{ip}/city").read().decode("utf-8")
        city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir = get_weatherInfo(
            request, city)
        return jumbotron(request, page, city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir)


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

    try:
        api_json2 = requests.get(
            "http://api.weatherstack.com/current?access_key=f4ec8c3283872a7de69e9ec1129bfebf&query=" + city).json()
        city = api_json2['location']['name']
        country = api_json2['location']['country']
        obsrvtime = api_json2['current']['observation_time']
        date = '-'.join(api_json2['location']
                        ['localtime'][:11].strip().split('-')[::-1])
        temp = str(api_json2['current']['temperature'])
        w_description = api_json2['current']['weather_descriptions']
        feelslike = api_json2['current']['feelslike']
        precip = api_json2['current']['precip']
        visibility = api_json2['current']['visibility']
        wind_speed = api_json2['current']['wind_speed']
        wind_degree = str(api_json2['current']['wind_degree']) + '°'

        wind_dir = api_json2['current']['wind_dir']

        # Make two list an used the zip function
        if wind_dir == 'S':
            wind_dir = 'South'
        elif wind_dir == 'SSE':
            wind_dir = 'South / South East'
        elif wind_dir == 'SE':
            wind_dir = 'South East'
        elif wind_dir == 'ESE':
            wind_dir = 'East / South East'
        elif wind_dir == 'E':
            wind_dir = 'East'
        elif wind_dir == 'ENE':
            wind_dir = 'East / North East'
        elif wind_dir == 'NE':
            wind_dir = 'North East'
        elif wind_dir == 'NNE':
            wind_dir = 'Norht / North East'
        elif wind_dir == 'N':
            wind_dir = 'North'
        elif wind_dir == 'NNW':
            wind_dir = 'North / North West'
        elif wind_dir == 'NW':
            wind_dir = 'Nort West'
        elif wind_dir == 'WNW':
            wind_dir = 'West / North West'
        elif wind_dir == 'W':
            wind_dir = 'West'
        elif wind_dir == 'WSW':
            wind_dir = 'West / South West'
        elif wind_dir == 'SW':
            wind_dir = 'South West'
        elif wind_dir == 'SSW':
            wind_dir = 'South / South West'

        return city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir

    except Exception as e:
        return city, country, "No Time Availible", "No Date Availible", "No Temp. Availible", w_description, "No Temp. Availible", percip, visibility, wind_speed, wind_degree, "No Wind Direction Availible"

# !!! Oke, this is getting ridiculous! There must be some technique I'm missing. Like *args or something


def jumbotron(request, page, city, country, obsrvtime, date, temp, w_description, feelslike, precip, visibility, wind_speed, wind_degree, wind_dir):
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
            aqi = "An error has occurred!"

    except Exception as e:
        api_json = "Error with API..."

    return render(request, f'{page}.html', {'api_json': api_json,
                                            'aqi': aqi, "category_color": category_color,
                                            "status_description": status_description,
                                            "city": city, "country": country,
                                            "obsrvtime": obsrvtime, "date": date, "temp": temp,
                                            "w_description": w_description, "feelslike": feelslike,
                                            "precip": precip, "visibility": visibility,
                                            "wind_speed": wind_speed, "wind_degree": wind_degree,
                                            "wind_dir": wind_dir
                                            })
