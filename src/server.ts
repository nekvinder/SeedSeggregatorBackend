const port = 8000

const imagesDirName = 'Images'

import express from 'express'
const { PythonShell } = require('python-shell')
var path = require('path')
const cors = require('cors')
var bb = require('express-busboy')
import { createProcessRecord, getProcessRecord, storagePath } from './services/db'

export const app = express()

bb.extend(app, {
  upload: true,
  path: storagePath + '/' + imagesDirName + '/',
  allowedPath: /./,
})

app
  .use(cors())
  .use(express.json())
  .use('/' + imagesDirName, express.static(path.join(storagePath, imagesDirName)))

const getImageDirPath = (req: any) => {
  return req.protocol + '://' + req.get('host') + '/' + imagesDirName + '/'
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
    const file = (req as any).files.file
    console.log(req.body, file)
    let options = {
      mode: 'text',
      pythonOptions: ['-u'],
      scriptPath: '',
      args: [file.file],
    }
    PythonShell.run('seeds.py', options, async function(err, result) {
      if (err) throw err
      result = JSON.parse(result)
      const dbData = await createProcessRecord(
        {
          imageName: [file.uuid, 'file', file.filename].join('/'),
          title: req.body.title,
          description: req.body.description,
          percentages: JSON.stringify(result.percentages),
        },
        getImageDirPath(req)
      )
      res.json(dbData)
    })
  } catch (error) {
    res.json(error)
  }
})

app.listen(port, () => console.log(`Server connected to ${port}`))
