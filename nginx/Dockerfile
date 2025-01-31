FROM nginx:alpine

# Remover a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nossa configuração
COPY default.conf /etc/nginx/conf.d/default.conf
