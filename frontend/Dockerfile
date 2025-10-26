FROM node:20-alpine

WORKDIR /app

COPY package.json tsconfig.json next.config.mjs tailwind.config.ts postcss.config.mjs ./
COPY app ./app
COPY components ./components
COPY lib ./lib
COPY public ./public

RUN npm install --legacy-peer-deps && npm run build

EXPOSE 3000
CMD ["npm", "run", "start", "--", "-H", "0.0.0.0"]
