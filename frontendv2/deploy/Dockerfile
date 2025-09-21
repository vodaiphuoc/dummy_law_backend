# Stage 1: Build 
FROM node:lts-alpine AS build
WORKDIR /app

COPY ./frontendv2/*.json .

COPY ./frontendv2/deploy/nginx ./nginx
COPY ./frontendv2/public  ./public
COPY ./frontendv2/src ./src
RUN echo ls -la
RUN npm install .
RUN npm run build 


# Stage 2: Serve 
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/dist/frontendv2/browser /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]

