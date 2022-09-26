### Парсер hh.ru на Django, учебный проект
<br>
Заполнение данных: python manage.py fill_db<br>
<br>
Изменения #4:<br>
- Добавлены тесты (faker, mixer)<br>
- Добавлены тесты на views<br>
- Добавлена проверка ролей пользователей<br>
<br>
Изменения #3:<br>
- Добавлена регистрация и авторизация пользователей на сайте<br>
- Добавлено требование авторизации при добавлении/изменении регионов<br>
- Удаление регионов возможно только для суперпользователя<br>
- Добавлена связь пользователей с запросом<br>
<br>
Изменения #2:<br>
- Добавлены cookies, запоминается последний запрос<br>
- Для учебных целей созданы формы просмотра/добавления/редактирования/удаления регионов(view написаны с использованием CBV)<br>
- Убраны дублирования в коде<br>
<br>
Изменения #1:<br>
- Подключены bootstrap-шаблоны из предыдущего проекта на flask<br>
- Доработаны шаблоны (адреса страниц, переходы, создан базовый шаблон, подключена статика, общие доработки html-шаблонов)<br>
- Сделана передача данных на страницы, обработка входных данных переведена на синтаксис шаблонизатора Django<br>
- Для учебных целей создана контактная форма
- Добавлена таблица с настройками, доработана таблица с регионами HH, доработано заполнение данных (python manage.py fill_db)<br>
