## Test

Curl command to send post request to the server
`curl -F "file=@ImagesSrc/DSC_0078.JPG" --location --request POST 'http://meet.nekvinder.com:8000'`

## Setup

```
sudo apt install npm
npm i
sudo npm i -g pm2
pip3 install opencv-python numpy
sudo apt install libgl1-mesa-glx
pm2 start server.js
```