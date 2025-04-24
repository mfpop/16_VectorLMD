from django.shortcuts import render


def index(request):
    """
    Render the main metrics dashboard showing lean manufacturing metrics.
    """
    context = {
        "active_page": "metrics",
    }
    return render(request, "metrics/index.html", context)
