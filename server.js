const express = require('express')
const app = express()
const { PythonShell } = require('python-shell')
var busboy = require('connect-busboy')
var path = require('path')
var fs = require('fs-extra')

app.use(busboy())
app.use(express.static(path.join(__dirname, 'Images/')))

app.post('/', (req, res, next) => {
  var fstream, uploadedFileName
  req.pipe(req.busboy)
  req.busboy.on('file', function (fieldname, file, filename) {
    console.log('Uploading: ' + filename)
    uploadedFileName = filename
    fstream = fs.createWriteStream(__dirname + '/Images/' + filename)
    file.pipe(fstream)
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
})

const port = 8000
app.listen(port, () => console.log(`Server connected to ${port}`))
