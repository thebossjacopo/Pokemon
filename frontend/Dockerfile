FROM node:20
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install
COPY frontend ./
RUN npm run build
ENV PORT=3000
EXPOSE 3000
CMD ["npm","start"]
