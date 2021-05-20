const port = 8000

import express from 'express'
const app = express()
const { PythonShell } = require('python-shell')
var busboy = require('connect-busboy')
var path = require('path')
var fs = require('fs-extra')
const { hostname } = require('os')

app.use(busboy())
app.use('/Images', express.static(path.join(__dirname, 'Images/')))

const getUrl = (req: any) => {
  return req.protocol + '://' + req.get('host') + req.originalUrl
}

app.post('/', (req, res, next) => {
  try {
    var fstream, uploadedFileName
    req.pipe((req as any).busboy)
    ;(req as any).busboy.on('file', function (fieldname, file, filename) {
      filename = filename.split('.')[0] + new Date().toISOString() + '.' + filename.split('.')[1]
      uploadedFileName = filename
      const fileFullPath = __dirname + '/Images/' + filename
      console.log(9, fileFullPath)
      fstream = fs.createWriteStream(fileFullPath)
      file.pipe(fstream)
      fstream.on('close', function (error) {
        console.log(error)
      }),
        fstream.on('close', function () {
          let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: [fileFullPath],
          }
          PythonShell.run('seeds.py', options, function (err, result) {
            if (err) throw err
            result = JSON.parse(result)
            result.imageName = getUrl(req) + result.imageName
            res.json(result)
          })
        })
    })
  } catch (error) {
    res.json(error)
  }
})

app.listen(port, () => console.log(`Server connected to ${port}`))
