from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from hh.models import Regions, Settings
from .forms import ContactForm
from django.core.mail import send_mail


def index_view(request):
    index_image = Settings.objects.all()[0].index_image
    return render(request, 'hh/index.html', context={'index_image': index_image})


def search_view(request):
    regions = Regions.objects.order_by('sort', 'region').values()
    query = 'python'  # заглушка
    region = 2  # заглушка
    return render(request, 'hh/search.html', context={'query': query, 'region': region, 'regions': regions})


def results_view(request):
    # заглушка
    query_data = {'query': 'python', 'region': 2, 'region_name': 'Санкт-Петербург', 'found': 0, 'page': 0, 'pages': 0}
    return render(request, 'hh/results.html', context={'query_data': query_data, 'stat': [], 'vac': []})


def vac_view(request):
    vac_url = ''  # заглушка
    vac = []  # заглушка
    return render(request, 'hh/vac.html', context={'vac_url': vac_url, 'vac': vac})


def contacts_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                name,
                f'Сообщение: {message}',
                'from@example.com',
                [email],
                fail_silently=True,
            )
            # return HttpResponseRedirect('/')
            return HttpResponseRedirect(reverse('djangohh:index'))

    else:
        form = ContactForm()
    return render(request, 'hh/contacts.html', context={'form': form})
