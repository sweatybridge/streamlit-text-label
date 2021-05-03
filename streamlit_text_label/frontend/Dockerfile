FROM node:16-alpine3.13

WORKDIR /frontend

COPY package.json .
COPY package-lock.json .
RUN npm install

CMD ["npm", "run", "start"]
