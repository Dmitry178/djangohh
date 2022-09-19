from django.core.management.base import BaseCommand
import os
from django.conf import settings
from hh.models import Regions, Settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Заполняем таблицу с настройками
        Settings.objects.all().delete()
        # path = os.path.join(settings.BASE_DIR, 'media', 'hh', 'index_image.jpg')
        path = 'hh/index_image.jpg'
        Settings(query_default='python', hh_region_id_default=2, index_image=path).save()
        # Settings.objects.create(query_default='python', hh_region_id_default=2, index_image=path)

        # Заполняем таблицу с регионами
        regions = Regions.objects.all()
        print('Найдено записей в таблице:', len(regions))

        data = [
            {'id': 0, 'region': 'везде', 'sort': 0},
            {'id': 1, 'region': 'Москва', 'sort': 1},
            {'id': 2, 'region': 'Санкт-Петербург', 'sort': 2},
            {'id': 3, 'region': 'Екатеринбург', 'sort': 9999},
            {'id': 4, 'region': 'Новосибирск', 'sort': 9999},
            {'id': 66, 'region': 'Нижний Новгород', 'sort': 9999},
            {'id': 88, 'region': 'Казань', 'sort': 9999},
            {'id': 104, 'region': 'Челябинск', 'sort': 9999},
            {'id': 78, 'region': 'Самара', 'sort': 9999},
            {'id': 68, 'region': 'Омск', 'sort': 9999},
            {'id': 76, 'region': 'Ростов-на-Дону', 'sort': 9999},
            {'id': 99, 'region': 'Уфа', 'sort': 9999},
            {'id': 72, 'region': 'Пермь', 'sort': 9999},
            {'id': 54, 'region': 'Красноярск', 'sort': 9999},
            {'id': 26, 'region': 'Воронеж', 'sort': 9999},
            {'id': 24, 'region': 'Волгоград', 'sort': 9999},
            {'id': 53, 'region': 'Краснодар', 'sort': 9999},
            {'id': 79, 'region': 'Саратов', 'sort': 9999},
            {'id': 95, 'region': 'Тюмень', 'sort': 9999},
            {'id': 96, 'region': 'Ижевск', 'sort': 9999},
            {'id': 11, 'region': 'Барнаул', 'sort': 9999},
            {'id': 98, 'region': 'Ульяновск', 'sort': 9999},
            {'id': 35, 'region': 'Иркутск', 'sort': 9999},
            {'id': 102, 'region': 'Хабаровск', 'sort': 9999},
            {'id': 29, 'region': 'Махачкала', 'sort': 9999},
            {'id': 112, 'region': 'Ярославль', 'sort': 9999},
            {'id': 22, 'region': 'Владивосток', 'sort': 9999}
        ]

        Regions.objects.all().delete()

        for item in data:
            try:
                Regions.objects.get(hh_region_id=item['id'])
                print(f"Регион {item['region']} уже добавлен в базу")
                continue
            except:
                pass

            try:
                Regions.objects.create(hh_region_id=item['id'], region=item['region'], sort=item['sort'])
                print(f"Добавлен регион: {item['region']}")
            except:
                print(f"Ошибка добавления региона {item['region']}")
