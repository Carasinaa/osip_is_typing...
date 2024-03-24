# Osip is typing...
## Описание проекта
Бот, выдающий на предложение пользователя строку из [стихов Осипа Мандельштама](https://rustih.ru/osip-mandelshtam/), подобранную в рифму.
Бота можно попробовать в телеграме по этому тегу: [@osip_is_typing_bot](https://t.me/osip_is_typing_bot)
Ссылка на [pythonanywhere](http://carasinaa.pythonanywhere.com/)

## Структура репозитория
- crawler.py — файл с кодом краулера
- output.csv — датафрейм с данными, спаршенными краулером
- morphs.py — код, отделяющий последнее слово строки и делящий его на слоги
- verses.py — код, делящий стихотворения на строки 
- папка bot
    - morphs.json — аутпут файла morphs.py со словарем
    - verses.json — аутпут файла verses.py со словарем
    - rhymes.py — код, подбирающий рифму и рандомное предложение
    - stats.py — статистика и графики
    - osip.py — основной код бота
    - osip.jpg, poses.png, wordcloud.png — картинка для бота и аутпуты stats.py с графиками

## Requirements
Дляустановки и запуска бота необходимы:
```sh
pip3 install telebot
pip3 install json
pip3 install pandas
pip3 install pymorphy2
pip3 install bs4
pip3 install string
pip3 install re
pip3 install random
```
