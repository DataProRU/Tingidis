# Tingidis
1. Создайте файл .env и заполните по примеру .env.example

2. Создайте виртуальное окружение
```terminal
python3 -m venv .venv
```

3. Запустите виртуальное окружение
```terminal
source .venv/bin/activate
```

4. Установить библиотеки
```terminal
pip install -r requirements.txt
```

5. Запустите docker-контейнер
```terminal
docker-compose up --build  
```

6. Запустите приложение
```terminal
uvicorn web_app.main:app --host 0.0.0.0 --port 8000 --reload
```

7. Запустите телеграм бота
```terminal
python3 bot.py
```

Документация:
http://127.0.0.1:8000/docs
