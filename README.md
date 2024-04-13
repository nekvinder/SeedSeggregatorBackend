# SeedSeggregatorService

A simple service on which you can upload images, and it will do a simple color based analysis on the image and retrun information if the iamge has met the criteria.

Application : This powers a mobile app which is used by employee's in Dal[https://en.wikipedia.org/wiki/Dal] Processing units, and the data is centralised and shared with administrator. 

- API implementation in Typescript. OpenCV operations, color analyser service in python.

### Setup

```Bash
sudo apt install npm
npm i
sudo npm i -g pm2
pip3 install opencv-python numpy
sudo apt install libgl1-mesa-glx
pm2 start server.js
```

### Constants

```JSON
{
    "dark_yellow" : [3,116,0,25,255,255],
    "light_yellow" : [24,100,0,38,255,255],
    "light_green" : [47,102,0,88,186,255],
    "dark_green" : [47,185,0,88,255,255]
}
```

## API

Curl command to send post request to the server
- `curl -F "file=@ImagesSrc/DSC_0078.JPG" -F "title=test title" -F "description=test text" --location --request POST 'http://meet.nekvinder.com:8005/seedsProcess'`
- `curl -F "file=@ImagesSrc/DSC_0078.JPG" -F "title=test title" -F "description=test text" --location --request POST 'http://localhost:8000/seedsProcess'`


## API endpoints

### Process Seeds File upload

- `/seedsProcess` -> POST

- Send Body

  ```JSON
  {
    "file":FileObject,
    "title":"NekvinderJaipur",
    "description":"10 may first sample"
  }
  ```

- Receive Data : JSON

### Admin Login

- `/adminLogin` -> POST

- Send Body

  ```JSON
  {
    "username":"admin",
    "password":"Pass123"
  }
  ```

- Receive Data : `true` or `false`
