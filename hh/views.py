import urllib
from types import NoneType
from urllib.parse import unquote, quote

import chardet as chardet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Regions, Queries, SkillsArray, Skills
from .forms import ContactForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.http import HttpResponse
from . import hh_api


def index_view(request):
    # index_image = Settings.objects.all()[0].index_image
    index_image = 'hh/index_image.jpg'
    header = 'парсер вакансий на hh.ru'

    # queries = Queries.objects.all().order_by('-id')[:10]
    queries = Queries.objects.select_related('region_id').order_by('-id')[:10]

    queries = [{'text': query.query, 'url': quote(query.query), 'hh_region_id': query.region_id.hh_region_id,
                'region': query.region_id.region} for query in queries]

    return render(request, 'hh/index.html', context={'index_image': index_image, 'header': header, 'queries': queries})


def search_view(request):
    regions = Regions.objects.order_by('sort', 'region').values()
    query_data = get_cookies(request)
    return render(request, 'hh/search.html',
                  context={'query': query_data['query'], 'region': query_data['region'], 'regions': regions})


def results_view(request):
    query_data = get_cookies(request)

    if request.method == 'POST':
        # для формы CBV: form.instance.user = request.user
        # print(request.user)
        query_data['page'] = 0
        query_data['query'] = str(request.POST['search']).lower()
        if request.POST['region'].isdigit():
            query_data['region'] = int(request.POST['region'])
        else:
            query_data['region'] = 0

        region_id = Regions.objects.get(hh_region_id=query_data['region'])

        if not len(Queries.objects.filter(query=query_data['query'], region_id=region_id)):
            query = Queries(query=query_data['query'], region_id=region_id)
            query.save()

        query_id = Queries.objects.get(query=query_data['query'], region_id=region_id)
    else:
        if 'stat' in dict(request.GET):  # формирование статистики
            # получаем словарь, где: ключи - навыки, значения - количество этих навыков в вакансиях
            skills = hh_api.get_skills(query_data['query'], query_data['region'])

            # делаем пакетное добавление навыков в таблицу, игнорируем ошибки дубликатов
            bulk_data_s = [Skills(skill=skill) for skill in skills.keys()]
            Skills.objects.bulk_create(bulk_data_s, ignore_conflicts=True)

            # получаем id навыков
            skills_data = Skills.objects.filter(skill__in=list(skills.keys())).all()

            # формируем список для добавления в таблицу SkillsArray
            region_id = Regions.objects.get(hh_region_id=query_data['region'])
            query_id = Queries.objects.get(query=query_data['query'], region_id=region_id)
            bulk_data_sa = [SkillsArray(query_id=query_id, skill_id=Skills(id=item.id), amount=skills[item.skill])
                            for item in skills_data]

            # удаляем старые данные, добавляем пакетно новые
            SkillsArray.objects.filter(query_id=query_id).delete()
            SkillsArray.objects.bulk_create(bulk_data_sa)

            '''
            # старый неоптимизированный код
            region_id = Regions.objects.get(hh_region_id=query_data['region'])
            query_id = Queries.objects.get(query=query_data['query'], region_id=region_id)
            SkillsArray.objects.filter(query_id=query_id).delete()

            for key, value in skills.items():
                skill = Skills.objects.filter(skill=key).first()
                if isinstance(skill, NoneType):
                    skill = Skills(skill=key)
                    skill.save()

                skill_id = Skills.objects.get(skill=key)
                SkillsArray.objects.create(query_id=query_id, skill_id=skill_id, amount=value)'''

        if 'next' in dict(request.GET):
            query_data['page'] = 0 if query_data['page'] + 1 >= query_data['pages'] else query_data['page'] + 1
        if 'prev' in dict(request.GET):
            query_data['page'] = query_data['pages'] - 1 if query_data['page'] - 1 < 0 else query_data['page'] - 1
        if 'page' in dict(request.GET):
            if request.GET.get('page').isdigit():
                page = int(request.GET.get('page'))
                if 0 < page <= query_data['pages']:
                    query_data['page'] = page - 1

        if 'query' in dict(request.GET) and 'hh_id' in dict(request.GET):
            query_data['query'] = request.GET.get('query')
            query_data['region'] = request.GET.get('hh_id')
            query_data['page'] = 0

        region_id = Regions.objects.get(hh_region_id=query_data['region'])
        query_id = Queries.objects.get(query=query_data['query'], region_id=region_id)

    found, pages, vac = hh_api.get_request(query_data)
    if found:
        query_data['found'] = found
        query_data['pages'] = pages

    region = region_id.region
    stat = get_skills_stat(query_id)

    # skills = hh_api.get_skills(query_data['query'], query_data['region'])
    # print(skills)

    html = render(request, 'hh/results.html',
                  context={'query_data': query_data, 'region': region, 'stat': stat, 'vac': vac})

    set_cookies(html, query_data)

    return html


def get_skills_stat(query_id):
    if isinstance(query_id, NoneType):
        return []

    # получаем сумму всех навыков
    amount = SkillsArray.objects.filter(query_id=query_id).aggregate(Sum('amount'))
    amount = amount['amount__sum']
    if not amount:
        return []

    # получаем список навыков
    min_percent = 1 * amount / 100.0
    skills = SkillsArray.objects.select_related('skill_id').filter(query_id=query_id). \
        filter(amount__gte=min_percent).\
        order_by('-amount', 'skill_id__skill').all()

    # упаковка полученных значений
    ret = [[skill.skill_id.skill, round(skill.amount * 100 / amount)] for skill in skills]

    return ret


# def vac_view(request, vac_id):
def vac_view(request):
    vac = []
    vac_url = ''
    if request.method == 'GET':
        if request.GET['id'].isdigit():
            vac, vac_url = hh_api.get_vac(request.GET['id'])

    return render(request, 'hh/vac.html', context={'vac': vac, 'vac_url': vac_url})


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
    paginate_by = 10

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
