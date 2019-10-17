from django.shortcuts import render

# Create your views here.
from top_app.models import App
from top_app.scrap import scrape_all, scrape_one


def home(request):
    # scrape_all()
    apps = App.objects.filter(is_top=True)
    return render(request, 'home.html', {'apps': apps})


def re_scrap(request):
    scrape_all()
    apps = App.objects.filter(is_top=True)
    return render(request, 'home.html', {'apps': apps})


def single_data(request):
    name = request.GET.get('id')
    try:
        app = App.objects.get(package_name=name)
        screen_sots = app.screen_shot.all()
        if not screen_sots:
            scrape_one(request.GET.get('id'))
    except App.DoesNotExist:
        app = scrape_one(request.GET.get('id'))

    return render(request, 'details.html', {'app': app, 'screen_shots': app.screen_shot.all(),
                                            'video': app.videos.all()})
