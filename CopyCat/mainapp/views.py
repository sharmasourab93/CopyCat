from django.http import HttpResponse


# Create your views here.
def index(request):
    response = "<h1>Hello To Django 3.0 World!</h1>"
    return HttpResponse(response)
