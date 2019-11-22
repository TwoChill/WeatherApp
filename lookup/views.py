from django.shortcuts import render
# Create your views here.
# (Brains behind the scene with python.
# Use python to reflect in our APP/WebPage)


def home(request):
    """Home Page"""
    import requests

    try:
        api_json = requests.get("https://api.waqi.info/feed/india/?token=d4d75f4262bb8bf35993a20496b828b963580311").json()
        try:
            aqi = api_json['data']['aqi']
            category_color = ''

            if aqi <= 50:
                aqi = "Good"
                category_color = "good"
            elif 51 <= aqi <= 100:
                aqi = "Moderate"
                category_color = "moderate"
            elif 101 <= aqi <= 150:
                aqi = "Unhealthy for Sensitive Groups"
                category_color = "usg"
            elif 151 <= aqi <= 200:
                aqi = "Unhealthy"
                category_color = "unhealthy"
            elif aqi <= 201 <= 300:
                aqi = "Very Unhealthy"
                category_color = "veryunhealthy"
            elif aqi > 300:
                aqi = "Hazardous"
                category_color = "hazardous"
        except Exception as e:
            aqi = "Error with getting data out of API..."

    except Exception as e:
        api_json = "Error with API..."

    return render(request, 'home.html', {'api_json': api_json, 'aqi': aqi, "category_color": category_color})


def aboutme(request):
    """About Me Page"""
    return render(request, 'aboutme.html', {})
