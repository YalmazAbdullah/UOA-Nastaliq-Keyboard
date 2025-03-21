# FROM node:20 AS builder
# WORKDIR /app
# COPY package.json package-lock.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# FROM nginx:alpine
# COPY --from=builder /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# FROM node:20-alpine as builder
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# # --- Production Stage ---
# FROM nginx:stable-alpine
# COPY --from=builder /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]


# FROM node:18-alpine as builder
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# # --- Production Stage ---
# FROM nginx:alpine
# RUN apk add --no-cache certbot certbot-nginx
# COPY --from=builder /app/dist /usr/share/nginx/html
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx/nginx.conf /etc/nginx/conf.d
# RUN mkdir -p /etc/letsencrypt
# EXPOSE 80
# EXPOSE 443
# COPY entrypoint.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/entrypoint.sh
# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# CMD ["nginx", "-g", "daemon off;"]

FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Set the API URL environment variable (for build-time)
ARG VITE_API_URL=/api  # Default to /api (custom location) - change if using a subdomain
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Production Stage ---
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist .
RUN npm install -g serve
EXPOSE 80
CMD ["serve", "-s", ".", "-l", "80"]