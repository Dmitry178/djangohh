### Оптимизация sql-запросов:<br>

Адрес страницы // Запросов до оптимизации // Запросов после оптимизации // Средство оптимизации
1. **главная страница** // 6 // 1 // select_related
2. **/results/** // 17 // 4 // select_related
3. **/results/?stat** // 523 // 15 // общая оптимизация, bulk_create

Остальные страницы выдают малое количество запросов, в оптимизации не нуждаются.<br>
Основной страницей для оптимизации являлась **results** с get-запросом **stat** (запуск формирования статистики).<br>
После оптимизации количество запросов уменьшилось более чем в 10 раз.
