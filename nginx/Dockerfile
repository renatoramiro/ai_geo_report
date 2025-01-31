FROM nginx:alpine

# Remover a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nossa configuração de desenvolvimento
COPY default.dev.conf /etc/nginx/conf.d/default.conf
