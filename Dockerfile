FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@11.4.0
RUN npm install --save-dev prisma@latest
RUN npm install @prisma/client@latest
RUN npx prisma generate
COPY . .
EXPOSE 3001
CMD ["npm", "start"]
