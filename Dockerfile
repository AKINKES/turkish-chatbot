FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install -g npm@latest
RUN npm install --save-dev prisma@latest
RUN npm install @prisma/client@latest
RUN npx prisma generate
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
