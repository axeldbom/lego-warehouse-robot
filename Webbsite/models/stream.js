var mongoose = require('mongoose')

var streamerSchema = mongoose.Schema({
  title: {
    type: String
  },
  name: {
    type: String
  },
  controlPassword: {
    type: String
  },
  socketID: {
    type: String,
    unique: true
  },
  sessionID: {
    type: String
  },
  expireAt: { type: Date, default: undefined }
})

var Stremer = module.exports = mongoose.model('Stremer', streamerSchema)

module.exports.getAllStreams = async function () {
  var streamerPool = await new Promise(function (resolve, reject) {
    Stremer.find(function (err, streamers) {
      if (err)reject()
      resolve(streamers)
    })
  }).catch(error => { console.log('caught', error) })
  if (streamerPool == undefined) return []
  return streamerPool.reverse()
}
module.exports.isAstreamer = async function (socketID) {
  var result = await new Promise(function (resolve, reject) {
    Stremer.find({socketID: socketID}, function (err, result) {
      if (err)reject()
      resolve(result)
    })
  }).catch(error => { console.log('caught', error) })
  return result.length >= 1
}
module.exports.removeStreamerFromSocketId = async function (socketID) {
  Stremer.deleteOne({socketID: socketID}, function (err) {
    if (err) throw (err)
    console.log('1 document deleted')
  })
}
module.exports.getStreamers = async function () {
  var result = await new Promise(function (resolve, reject) {
    Stremer.find(function (err, streams) {
      if (err)reject()

      resolve(streams)
    })
  }).catch(error => { console.log('caught', error) })
  if (result == undefined) return []
  return result.reverse()
}

