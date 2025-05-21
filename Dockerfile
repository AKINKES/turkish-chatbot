FROM mintplexlabs/anythingllm:railway
RUN npm install -g npm@11.4.0
RUN npm install --save-dev prisma@latest
RUN npm install @prisma/client@latest
RUN npx prisma generate
EXPOSE 3001
