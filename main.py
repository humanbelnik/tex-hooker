import requests
import os
import yaml
import re
import browser_cookie3

def download_zip(url, cookies):
    # Добавляем '/download/zip' к URL
    full_url = f"{url}/download/zip"
    
    try:
        # Выполняем GET-запрос с куками
        response = requests.get(full_url, cookies=cookies)
        response.raise_for_status()  # Проверяем на наличие ошибок
        
        # Сохраняем содержимое в файл
        filename = "downloaded_file.zip"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Файл успешно загружен и сохранен как {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке файла: {e}")



# Функция для замены переменных окружения
def replace_env_vars(value):
    # Используем регулярное выражение для поиска переменных окружения
    return re.sub(r'\${(.*?)}', lambda match: os.getenv(match.group(1), ''), value)

# Загружаем настройки из файла conf.yaml
with open('conf.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Применяем замену переменных окружения
for session_name, session_data in config['sessions'].items():
    session_data['path'] = replace_env_vars(session_data['path'])

# Пример доступа к данным
browser = config['browser']
sessions = config['sessions']

# Выводим настройки
print(f"Используемый браузер: {browser}")

for session_name, session_data in sessions.items():
    print(f"Сессия: {session_name}")
    print(f"  Тег: {session_data['tag']}")
    print(f"  Ссылка: {session_data['link']}")
    print(f"  Путь: {session_data['path']}")


# Получаем куки из Firefox для конкретного домена
cookies = browser_cookie3.firefox(domain_name='overleaf.com')

# Преобразуем куки в словарь для использования в запросах
cookies_dict = {cookie.name: cookie.value for cookie in cookies}
print(cookies_dict)

download_zip("https://www.overleaf.com/project/672366509c5311ddb4355f7b", cookies)
