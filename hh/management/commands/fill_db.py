from django.core.management.base import BaseCommand
from hh.models import Regions, Queries, Skills, SkillsArray


class Command(BaseCommand):

    def handle(self, *args, **options):
        regions = Regions.objects.all()
        print('Найдено записей в таблице:', len(regions))

        data = {
            0: 'везде',
            1: 'Москва',
            2: 'Санкт-Петербург',
            3: 'Екатеринбург',
            4: 'Новосибирск',
            66: 'Нижний Новгород',
            88: 'Казань',
            104: 'Челябинск',
            78: 'Самара',
            68: 'Омск',
            76: 'Ростов-на-Дону',
            99: 'Уфа',
            72: 'Пермь',
            54: 'Красноярск',
            26: 'Воронеж',
            24: 'Волгоград',
            53: 'Краснодар',
            79: 'Саратов',
            95: 'Тюмень',
            96: 'Ижевск',
            11: 'Барнаул',
            98: 'Ульяновск',
            35: 'Иркутск',
            102: 'Хабаровск',
            29: 'Махачкала',
            112: 'Ярославль',
            22: 'Владивосток'
        }

        for key, value in data.items():
            try:
                Regions.objects.get(hh_region_id=key)
                print(f'Регион {value} уже добавлен в базу')
                continue
            except:
                pass

            try:
                Regions.objects.create(hh_region_id=key, region=value)
                print(f'Добавлен регион: {value}')
            except:
                print(f'Ошибка добавления региона {value}')

        # Regions.objects.all().delete()
