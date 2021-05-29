import { Sequelize } from 'sequelize-typescript'
import { Table, Column, Model, AllowNull } from 'sequelize-typescript'

@Table({ timestamps: true })
class ImageProcessRecord extends Model {
  @Column
  title: string

  @AllowNull
  @Column
  description: string

  @Column
  imageName: string

  @Column
  percentages: string
}

export const storagePath = '/usr/data'
const sequelize = new Sequelize({
  database: 'some_db',
  dialect: 'sqlite',
  username: 'root',
  password: '',
  storage: storagePath + '/db.sqlite',
  models: [ImageProcessRecord], // or [Player, Team],
  logging: true,
})

export const connect = async () => {
  try {
    await sequelize.authenticate()
    await sequelize.sync()
  } catch (error) {
    console.error('Unable to connect to the database:', error)
  }
}
connect()

export const createProcessRecord = async (options: { title: string; description: string; imageName: string; percentages: string }, url?: string) => {
  const record = await ImageProcessRecord.create({
    title: options.title,
    description: options.description,
    imageName: options.imageName,
    percentages: options.percentages,
  })
  return parseRecords(record, url).toJSON()
}

export const getProcessRecord = async (url?: string) => {
  const record = await ImageProcessRecord.findAll({ order: [['createdAt', 'DESC']] })
  return record.map((val) => parseRecords(val, url))
}

export function parseRecords(val: any, url?: string) {
  val.percentages = JSON.parse(val.percentages)
  if (url) val.imageName = url + val.imageName
  return val
}
