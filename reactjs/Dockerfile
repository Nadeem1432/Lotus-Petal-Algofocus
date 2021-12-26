# pull official base image
FROM node:14.18.1

# set working directory
WORKDIR /home/ubuntu/reactjs

# add `/app/node_modules/.bin` to $PATH
ENV PATH /home/ubuntu/reactjs/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY yarn.lock ./
RUN  yarn install --silent
RUN  yarn global add react-scripts@3.4.1 -g --silent

# add app
COPY . ./

# start app
CMD ["yarn", "start"]

