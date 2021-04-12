FROM nikolaik/python-nodejs:latest
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN pip3 install numpy
RUN pip3 install opencv-python
COPY . .
EXPOSE 8000
CMD [ "node", "server.js" ]