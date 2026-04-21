# Сайт-визитка для мастера по наращиванию ресниц

Готовый сайт для размещения в Docker на сервере Ubuntu.

## Структура проекта

```
lash-master-site/
├── html/
│   └── index.html          # Главная страница сайта
├── css/
│   └── style.css           # Стили сайта
├── js/
│   └── script.js           # JavaScript функционал
├── images/                  # Директория для изображений
├── Dockerfile              # Docker конфигурация
└── docker-compose.yml      # Docker Compose конфигурация
```

## Быстрый старт

### 1. Сборка и запуск через Docker Compose (рекомендуется)

```bash
cd lash-master-site
docker-compose up -d --build
```

Сайт будет доступен по адресу: http://localhost

### 2. Сборка и запуск через Docker

```bash
cd lash-master-site
docker build -t lash-master-site .
docker run -d -p 80:80 --name lash-master-website lash-master-site
```

Сайт будет доступен по адресу: http://localhost

## Развертывание на сервере Ubuntu

### Требования
- Ubuntu Server 20.04 или новее
- Docker
- Docker Compose

### Установка Docker и Docker Compose

```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version
```

### Развертывание сайта

1. Скопируйте файлы проекта на сервер:
```bash
scp -r lash-master-site user@your-server-ip:/home/user/
```

2. Подключитесь к серверу:
```bash
ssh user@your-server-ip
```

3. Перейдите в директорию проекта и запустите:
```bash
cd lash-master-site
docker-compose up -d --build
```

4. Проверьте статус контейнера:
```bash
docker-compose ps
```

5. Посмотрите логи:
```bash
docker-compose logs -f
```

## Управление контейнером

```bash
# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f

# Обновление (после изменений в коде)
docker-compose up -d --build
```

## Настройка домена (опционально)

Для использования собственного домена:

1. Купите домен у регистратора
2. Настройте A-запись на IP вашего сервера
3. Установите SSL сертификат с помощью Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Кастомизация

### Изменение контактной информации

Откройте `html/index.html` и найдите секцию `<section id="contact">`. Измените:
- Телефон
- WhatsApp
- Telegram
- Instagram
- Адрес
- Время работы

### Добавление фотографий

1. Поместите ваши фотографии в папку `images/`
2. Замените заглушки в HTML коде на пути к вашим изображениям:
```html
<img src="images/your-photo.jpg" alt="Описание">
```

### Изменение цветовой схемы

Откройте `css/style.css` и измените основные цвета:
- `#d4a5a5` - основной акцентный цвет (розовый)
- `#f5e6e6`, `#ffe4e1` - цвета фона

## Особенности сайта

- ✅ Адаптивный дизайн (мобильные, планшеты, десктоп)
- ✅ Плавная прокрутка к секциям
- ✅ Мобильное меню (бургер)
- ✅ Форма записи (с имитацией отправки)
- ✅ Секции: Главная, Обо мне, Услуги, Портфолио, Отзывы, Контакты
- ✅ Анимации при скролле
- ✅ SEO-оптимизированная структура

## Техническая информация

- **Веб-сервер**: Nginx (Alpine)
- **Порт**: 80
- **Размер образа**: ~25 MB
- **Статический сайт**: HTML, CSS, JavaScript

## Поддержка

Для вопросов и предложений обращайтесь к разработчику.

---

© 2024 Мастер по наращиванию ресниц
