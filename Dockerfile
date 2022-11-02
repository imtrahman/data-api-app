FROM public.ecr.aws/docker/library/node:alpine3.14

EXPOSE 3000

COPY . /app

WORKDIR /app

RUN npm install && apk --no-cache -U add curl

CMD ["node", "app.js"]
