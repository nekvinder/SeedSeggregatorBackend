## Test

Curl command to send post request to the server
`curl -F "file=@ImagesSrc/DSC_0078.JPG" --location --request POST 'http://meet.nekvinder.com:8000'`
`curl -F "file=@ImagesSrc/DSC_0078.JPG" --location --request POST 'http://localhost:8000'`
## Setup

```
sudo apt install npm
npm i
sudo npm i -g pm2
pip3 install opencv-python numpy
sudo apt install libgl1-mesa-glx
pm2 start server.js
```


## constants

{
    "dark_yellow" : [3,116,0,25,255,255],
"light_yellow" : [24,100,0,38,255,255],
"light_green" : [47,102,0,88,186,255],
"dark_green" : [47,185,0,88,255,255]
}