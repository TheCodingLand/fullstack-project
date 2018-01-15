


# install latest node
# https://hub.docker.com/_/node/
FROM node:latest

# create and set app directory
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
COPY . /usr/src/app/
# install app dependencies
# this is done before the following COPY command to take advantage of layer caching
COPY package.json /usr/src/app/
RUN npm install

# copy app source to destination container
COPY . /usr/src/app/
COPY ./webpack.config/* /usr/src/app/node-modules/react-scripts/config/

# expose container port
EXPOSE 3000
EXPOSE 3001
