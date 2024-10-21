# Accu_py_ext_2

Это Flask-приложение для получения данных о погоде с использованием AccuWeather API. 

### 1. Клонирование репозитория


```bash
git clone https://github.com/chellick/Accu_py_ext_2.git
cd Accu_py_ext_2
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
```


На Windows:

```bash
venv\Scripts\activate
```

На macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Пробросьте ваш ключ от [AccuWeatherAPI](https://developer.accuweather.com/user/login)

Создайте файл `.env`

в него вставьте: `API_KEY=your_accuweather_api_key`

---------

```
Accu_py_ext_2/
├── app/
│   ├── app.py
│   ├── handlers/
│   │   ├── location.py
│   │   └── model.py
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       ├── index.html
│       └── weather_result.html
├── .gitignore
├── README.md
└── requirements.txt

```
--------


PS.
Никакого WSGI типа gunicorn'a нет. Фласк нативно поддерживает рендер. 