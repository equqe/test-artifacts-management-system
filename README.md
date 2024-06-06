# test-artifacts-management-system by june 1st
test artifacts management system on Django.

# how-to

```
git clone https://github.com/equqe/test-artifacts-management-system

cd test-artifacts-management-system

docker-compose build

docker-compose up
```

### in case of errors


make sure DATABASE data in settings.py is similar to this:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": "5432",
    }
}
```

# main page `127.0.0.1:8000`, register page `127.0.0.1:8000/accounts/register`


![image](https://github.com/equqe/test-artifacts-management-system/assets/145790372/e0d9810c-eb1e-4c83-85e5-accc4547c5e0)



![image](https://github.com/equqe/test-artifacts-management-system/assets/145790372/a258b7a5-4ed9-45f2-aee3-4736a18401ff)


## :::CHANGELOG

исправлена ошибка при регистрации Group matching query does not exist, добавление юзера в обе группы, ошибка при генерации отчета багрепорта, изменена ориентация листа pdf на горизонтальную, шаги можно добавлять в любом количестве и редактировать имеющиеся
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!сейчас коммичу версию, где в меню редактирования нельзя добавлять новые шаги к тесткейсам, чтобы не потеряться в версиях
примерно через 20 минут(возможно поменьше) будет закоммичен фикс с возможностью добавлять шаги в меню редактирования кейса

# описание архитектуры

<details>
  <summary><b>`fonts/`</b></summary>
  <p>Содержит кириллический шрифт Arial для правильного отображения символов при генерации PDF отчета</p>
  <ul>
    <li><b>`arial.ttf`</b></li>
    <p>Шрифт</p>
  </ul>
</details>
<details>
  <summary><b>`nginx/`</b></summary>
  <p>Этот каталог содержит конфигурацию веб-сервера Nginx(nginx.conf), с помощью которого работает Django-приложение, запущенное на Docker.</p>
  <ul>
    <li><b>`nginx.conf`</b></li>
    <p>Конфиг веб-сервера Nginx</p>
  </ul>
</details>
<details>
  <summary><b> `systemart/` </b></summary>
  <p>Это корневой каталог проекта, содержащий весь код приложения, шаблоны и статические файлы.</p>
  <ul>
    <li>
      <details>
        <summary><b>`apps/`</b></summary>
        <p>Папка со всеми созданными приложениями Django</p>
        <ul>
          <li>
            <details>
              <summary><b>`main/`</b></summary>
              <p>Папка приложения main - основного приложения со всем функционалом</p>
              <ul>
                <li>
                  <details>
                    <summary><b>`migrations/`</b></summary>
                    <p>Миграции Django для БД Postgres</p>
                  </details>
                </li>
                <li>
                  <details>
                    <summary><b>`static/`</b></summary>
                    <p>Содержит статические файлы проекта - HTML, JS, CSS</p>
                    <ul>
                      <li>
                        <details>
                          <summary><b>`css/`</b></summary>
                          <p>Содержит CSS(стили) для шаблонов</p>
                          <ul>
                            <li><b>`main.css`</b></li>
                            <p>Файл со всеми CSS-стилями</p>
                          </ul>
                        </details>
                      </li>
                      <li>
                        <details>
                          <summary><b>`js/`</b></summary>
                          <p>Содержит JavaScript для шаблонов</p>
                          <ul>
                            <li><b>`main.js`</b></li>
                            <p>Скрипт</p>
                            <li><b>`jquery-3.6.0.min.js`</b></li>
                            <p>Плагин JQuery для JavaScript</p>
                          </ul>
                        </details>
                      </li>
                    </ul>
                  </details>
                </li>
                <li>
                  <details>
                    <summary><b>`templates/`</b></summary>
                    <p>Содержит HTML-шаблоны страниц</p>
                    <ul>
                      <li><b>`main/`</b></li>
                      <p>Содержит шаблоны приложения main</p>
                      <li><b>`registration/`</b></li>
                      <p>Содержит шаблоны для авторизации</p>
                    </ul>
                  </details>
                </li>
                <li><b>`forms.py`</b></li>
                <p>Все формы приложения(авторизация, создание проектов, изменение и др.)</p>
                <li><b>`models.py`</b></li>
                <p>Модели для БД(пользователь, тесткейсы, проекты и др.)</p>
                <li><b>`views.py`</b></li>
                <p>Все представления приложения, т.е. ответы на запросы к приложению</p>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary><b>`sysart/`</b></summary>
              <p>Папка приложения main - основного приложения со всем функционалом</p>
              <ul>
                <li><b>`settings.py`</b></li>
                <p>
Основные настройки приложения - данные для подключения к БД, включение/отключение режима дебага, подключение приложений, middleware и т.д.
                </p>
                <li><b>`urls.py`</b></li>
                <p>Все URL-адреса, доступные для посещения</p>
              </ul>
            </details>
          </li>
        </ul>
      </details>
    </li>
  </ul>
</details>

<details>
  <summary><b>`Dockerfile & docker-compose.yml`</b></summary>
  <p>Конфигурация Docker для запуска контейнеров с Django, Postgres и Nginx</p>
</details>

<details>
  <summary><b>`wait-for-it.sh`</b></summary>
  <p>
    Bash-скрипт, который предотвращает появление ошибок, связанных с невозможностью Django подключиться к Postgres из-за того, что Django запускается раньше, чем Postgres
  </p>
</details>

# пример генерируемого отчета pdf

![image](https://github.com/equqe/test-artifacts-management-system/assets/145790372/569dfa21-e335-4ef9-b660-e589a8a2ce44)

