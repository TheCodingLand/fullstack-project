FROM nginx:alpine
COPY ./static /usr/share/nginx/html
ADD ./nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]