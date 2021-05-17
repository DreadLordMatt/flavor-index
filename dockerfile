FROM node:lts-alpine

LABEL matt benoit <https://github.com/DreadLordMatt/flavor-index>

# install simple http server for serving static content
RUN npm install -g lite-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

EXPOSE 3000
CMD [ "lite-server", "dist" ]