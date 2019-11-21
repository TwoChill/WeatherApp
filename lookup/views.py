from django.shortcuts import render

# Create your views here.
# (Brains behind the scene with python. Use python to reflect in our APP/WebPage)

def home(request):
    return render(request, 'home.html', {})

def aboutme(request):
	return render(request, 'aboutme.html', {})
