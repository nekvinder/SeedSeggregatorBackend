const port = 8000

const express = require('express')
const app = express()
const { PythonShell } = require('python-shell')
var busboy = require('connect-busboy')
var path = require('path')
var fs = require('fs-extra')
const { hostname } = require('os')

app.use(busboy())
app.use('/Images', express.static(path.join(__dirname, 'Images/')))
app.use(function (req, res, next) {
  req.getUrl = function () {
    return req.protocol + "://" + req.get('host') + req.originalUrl;
  }
  return next();
});


app.post('/', (req, res, next) => {
  try {
console.log(req.getUrl())
    var fstream, uploadedFileName
    req.pipe(req.busboy)
    req.busboy.on('file', function (fieldname, file, filename) {
      filename = filename.split('.')[0] + new Date().toISOString() + '.' + filename.split('.')[1]
      uploadedFileName = filename
      fstream = fs.createWriteStream(__dirname + '/Images/' + filename)
      file.pipe(fstream)
      fstream.on('close', function (error) {
        console.log(error)
      }),
        fstream.on('close', function () {
          console.log('Upload Finished of ' + filename)
          let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: ['Images/' + uploadedFileName],
          }

          PythonShell.run('seeds.py', options, function (err, result) {
            if (err) throw err
            console.log('result: ', result.toString())
            res.json(result)
          })
        })
    })
  } catch (error) {
    res.json(error)
  }
})

app.listen(port, () => console.log(`Server connected to ${port}`))
