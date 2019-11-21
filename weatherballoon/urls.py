from django.contrib import admin
# INCLUDE will allow us the include other URLs from other apps in our project, in this file.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # grab everything in this the new lookup.urls file and pull it in this main one
    path('', include('lookup.urls')),
]
