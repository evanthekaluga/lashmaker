# Dockerfile для сайта мастера по наращиванию ресниц

FROM nginx:alpine

# Копируем файлы сайта в директорию nginx
COPY html/ /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/

# Создаем директорию для изображений и копируем файлы, если они есть
RUN mkdir -p /usr/share/nginx/html/images
COPY images/ /usr/share/nginx/html/images/ || true

# Копируем конфигурацию nginx с прокси для бэкенда
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
