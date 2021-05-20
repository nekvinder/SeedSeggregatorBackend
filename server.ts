const port = 8000

import * as express from 'express'
const { PythonShell } = require('python-shell')
var busboy = require('connect-busboy')
var path = require('path')
var fs = require('fs-extra')
const { hostname } = require('os')
const cors = require('cors')
import { connect, createProcessRecord, getProcessRecord } from './services/db'

export const app = require('express')()

app.use(busboy()).use(express.json()).use(cors())
app.use('/Images', express.static(path.join(__dirname, 'Images/')))

const getImageDirPath = (req: any) => {
  return req.protocol + '://' + req.get('host') + '/Images/'
}

app.get('/history', async (req, res, next) => {
  res.json(await getProcessRecord(getImageDirPath(req)))
})

app.post('/adminLogin', (req, res, next) => {
  const { username, password } = req.body
  res.json(username == 'admin' && password == 'Pass123')
})

app.post('/seedsProcess', (req, res, next) => {
  try {
    var fstream
    req.pipe((req as any).busboy)
    ;(req as any).busboy.on('file', function (fieldname, file, filename) {
      filename = filename.split('.')[0] + new Date().toISOString() + '.' + filename.split('.')[1]
      const fileFullPath = __dirname + '/Images/' + filename
      fstream = fs.createWriteStream(fileFullPath)
      file.pipe(fstream)
      fstream.on('close', function (error) {
        console.log(error)
      }),
        fstream.on('close', async function () {
          let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: [fileFullPath],
          }
          PythonShell.run('seeds.py', options, async function (err, result) {
            if (err) throw err
            result = JSON.parse(result)
            console.log(req.body)

            // result.imageName = getUrl(req) + result.imageName
            const dbData = await createProcessRecord(
              {
                imageName: filename,
                title: req.body.title,
                description: req.body.description,
                percentages: JSON.stringify(result.percentages),
              },
              getImageDirPath(req)
            )
            res.json(dbData)
          })
        })
    })
  } catch (error) {
    res.json(error)
  }
})

app.listen(port, () => console.log(`Server connected to ${port}`))
