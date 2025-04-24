from django.shortcuts import render


# Create your views here.
def home(request):
    # Adding explicit context data
    context = {
        "title": "Home",
        "content_block": "This is the home content",
    }
    return render(request, "home/home.html", context)
