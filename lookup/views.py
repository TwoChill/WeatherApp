from django.shortcuts import render
# Create your views here.
# (Brains behind the scene with python.
# Use python to reflect in our APP/WebPage)

# Might use visitors IP, get visitors location, put in city var.


def jumbotron(request, city):
    """Jumbotron"""
    import requests

    try:
        api_json = requests.get("https://api.waqi.info/feed/" + city + "/?token=d4d75f4262bb8bf35993a20496b828b963580311").json()

        try:
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
            aqi = "Error with getting data out of API..."

    except Exception as e:
            api_json = "Error with API..."

    return render(request, 'home.html', {'api_json': api_json, 'aqi': aqi, "category_color": category_color, "status_description": status_description})


def home(request):
    """Home Page"""
    # POST and GET (Brush up on HTML5 and CSS Forms)
    if request.method == "POST":
        city = request.POST['citylookup']
        return jumbotron(request, city)

    else:
        city = "Amsterdam"
        return jumbotron(request, city)


def aboutme(request):
    """About Me Page"""
    return render(request, 'aboutme.html', {})
