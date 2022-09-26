from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Regions, Settings
from .forms import ContactForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.http import HttpResponse


def index_view(request):
    # index_image = Settings.objects.all()[0].index_image
    index_image = 'hh/index_image.jpg'
    return render(request, 'hh/index.html', context={'index_image': index_image})


def search_view(request):
    regions = Regions.objects.order_by('sort', 'region').values()
    query_data = get_cookies(request)
    return render(request, 'hh/search.html',
                  context={'query': query_data['query'], 'region': query_data['region'], 'regions': regions})


def results_view(request):
    print(type(request))
    query_data = get_cookies(request)
    # query_data = {'region_name': 'Санкт-Петербург', 'region': 0, 'found': 0, 'page': 0, 'pages': 0}
    if request.method == 'POST':
        # для формы CBV: form.instance.user = request.user
        print(request.user)
        query_data['query'] = request.POST['search']
        if request.POST['region'].isdigit():
            query_data['region'] = int(request.POST['region'])
        # Queries.objects.
    else:
        pass

        # query_data['region_name'] = 'Санкт-Петербург'
        # print(query_data)
        # return render(request, 'hh/results.html', context={'query_data': query_data, 'stat': [], 'vac': []})

    html = render(request, 'hh/results.html', context={'query_data': query_data, 'stat': [], 'vac': []})
    set_cookies(html, query_data)
    return html


def vac_view(request, vac_id):
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


@user_passes_test(lambda u: u.is_superuser)
# @login_required
def history_view(request):
    return render(request, 'hh/history.html', context={})


def set_cookies(html, query_data: {}):
    for key, value in query_data.items():
        html.set_cookie(key, str(value), max_age=60 * 60 * 24 * 15)


def get_cookies(request) -> {}:
    query_data = {'query': 'python', 'region': 0, 'found': 0, 'page': 0, 'pages': 0}
    for key in query_data:
        cookie = request.COOKIES.get(key)
        if cookie is None:
            continue
        try:
            cookie = int(cookie) if isinstance(query_data[key], int) else str(cookie)
        except:
            continue
        query_data[key] = cookie
    return query_data


class NameContextMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Регионы'
        return context


class RegionsListView(ListView, NameContextMixin):
    model = Regions
    template_name = 'hh/regions_list.html'
    context_object_name = 'regions'

    def get_queryset(self):
        return Regions.objects.all()


class RegionsDetailView(DetailView, NameContextMixin):
    model = Regions
    template_name = 'hh/regions_detail.html'

    def get(self, request, *args, **kwargs):
        self.region_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Regions, pk=self.region_id)


class RegionsCreateView(LoginRequiredMixin, CreateView, NameContextMixin):
    fields = '__all__'
    model = Regions
    success_url = reverse_lazy('djangohh:region_list')
    template_name = 'hh/regions_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RegionsUpdateView(LoginRequiredMixin, UpdateView):
    fields = '__all__'
    model = Regions
    success_url = reverse_lazy('djangohh:region_list')
    template_name = 'hh/regions_create.html'


class RegionsDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'hh/regions_delete.html'
    model = Regions
    success_url = reverse_lazy('djangohh:region_list')

    def test_func(self):
        return self.request.user.is_superuser
