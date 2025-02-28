FROM node:18

WORKDIR /usr/src/app

COPY src/package*.json ./

RUN npm install

COPY src/ .
COPY flag.txt .

EXPOSE 5000

CMD ["sh", "-c", "node app.js & node admin.js"]
