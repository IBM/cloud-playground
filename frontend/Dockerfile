FROM node:12-alpine as build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm install -g @angular/cli
RUN ng build --configuration production --output-path=/dist

################
# Run in NGINX #
################
# A special NGINX image due to current limitations, that should be removed soon
FROM nginxinc/nginx-unprivileged

USER root
COPY --from=build /dist /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx

USER nginx
# When the container starts, replace the env.js with values from environment variables
CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/json/runtime_template.json > /usr/share/nginx/html/assets/json/runtime.json && exec nginx -g 'daemon off;'"]
