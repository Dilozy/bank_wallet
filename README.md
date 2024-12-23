# Проект Банковский кошелек

## Обзор
Этот API предоставляет функциональность для отображения баланса на кошельке и выполнения операций (депозит и снятие средств) с кошельком.


## Установка
### 1. Клонируйте репозиторий с Git
`git clone https://github.com/Dilozy/bank_wallet`

### 2. Создайте .env файл в корневой папке проекта со следующей структурой
    DB_NAME= "Имя базы данных"
    DB_USER= "Пользователь базы данных"
    DB_PASSWORD= "Пароль для доступа к базе данных"
    DB_HOST="db"
    DB_PORT="5432"

    DJANGO_SECRET_KEY= Секретный ключ Django приложения, генерируется командой 
    
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    
    DEBUG="False"
    DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1"

### 3. Соберите и запустите контейнеры командой
`docker-compose up -d`

### 4. Выполните начальные миграции для базы данных
`docker-compose exec app python manage.py migrate`

### 5. После запуска контейнеров приложение доступно по адресу
    http://127.0.0.1

### 6. Остановка контейнеров
Когда вы закончите работу, остановите контейнеры командой: `docker-compose down`. Это остановит и удалит контейнеры, но сохранит образы.

## Описание API
### 1. **Показать информацию о кошельке**  
#### `GET /wallets/<wallet_uuid>/`
Этот эндпоинт используется для получения текущего баланса конкретного кошелька, идентифицируемого его `wallet_uuid`.

#### Запрос:
- **Параметр URL:**
  - `wallet_uuid` (обязательный): UUID кошелька, для которого нужно получить информацию.

#### Ответ:
- **Код состояния:** `200 OK`
- **Тело ответа:**
  ```json
  {
      "wallet_id": "string",
      "balance": "decimal"
  }


### 2. **Операция с кошельком**  
#### `POST /wallets/<wallet_uuid>/operation/`
Этот эндпоинт позволяет пользователю выполнить операцию с кошельком — депозит или снятие средств. Тип операции и сумма передаются в теле запроса.

#### Запрос:
- **Параметр URL:**
  - `wallet_uuid` (обязательный): UUID кошелька, с которым выполняется операция.
- **Тело запроса:**
  ```json
  {
      "operationType": "string",  // "DEPOSIT" или "WITHDRAW"
      "amount": "decimal"
  }