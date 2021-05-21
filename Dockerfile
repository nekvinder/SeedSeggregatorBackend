FROM nikolaik/python-nodejs:latest
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN apt-get update && apt-get install -y python3-opencv
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN pip3 install numpy
RUN pip3 install opencv-python
COPY ./dist .
EXPOSE 8000
CMD [ "node", "server.js" ]