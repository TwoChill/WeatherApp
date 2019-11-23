from django.urls import path
from. import views
urlpatterns = [
    # This is the place were you will create new url when we create a new webpage.
    # Need three things in DJANGOfor creating a webstie
    # 1. the URL To poit the thing to
    # 2. the actual HTML PAGE.
    # 3. to VIEWS (Brains behind the scene with python. Use python to reflect in our APP/WebPage)
    path('', views.home, name='home'),
    # path('aboutme.html', views.aboutme, name='aboutme'),



]
