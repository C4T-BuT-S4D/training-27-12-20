FROM node:dubnium

WORKDIR /app
ADD package.json .
ADD yarn.lock .
RUN yarn install

COPY index.js .

CMD ["node", "index.js"]
