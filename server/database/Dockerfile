FROM node:24-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY app.js ./
COPY data ./data
USER node
ENV HOST=0.0.0.0 PORT=3030 NODE_ENV=production
EXPOSE 3030
CMD ["node","app.js"]
