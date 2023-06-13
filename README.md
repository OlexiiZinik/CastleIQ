# CastleIQ
Система керування розумним будинком

Тести не працюють через помилку в TortoiseORM. Взагалі тортойс кривий.


## Деплой для розробки
```bash
git clone https://github.com/OlexiiZinik/CastleIQ.git
cd CastleIQ
git checkout dev
```

Переіменовуємо **example.env** на **.env**

Вставляємо туди приватний ключ ключ та строку підключення до бд (важливо викорисовувати postgesql)

**Дуже важливо використовувати python 3.10 або старше**
```bash
cd CastleIQ \HUB
python3.10 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Встановлюємо бібліотеку подій
```bash
cd ../CastleIQ \Events
pip install -e .
cd ../CastleIQ \HUB
```

Генеруємо самопідписні ssl сертифікати за допомогою ``mkcert``

Вставляємо їх у **runner.py**

У разі необхідності застосовуємо міграції
```bash
aerich upgrade
```

Запускаємо
```bash
python runner.py
```

створюємо користувача
```bash
python create_user.py
```


## Запускаємо UI
```bash
cd CastleIQ \UI
npm install
npm run host
```

PS слід перевірити чи співпадає API_URL у vuex обробниках з вашим URL до CastleIQ HUB

пристрої на даний момент підключаються лише руцями через API
ендпоінт 
``https://ВашСерверАпі/dev_api/connect_new``