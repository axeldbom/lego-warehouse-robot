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
  robotClient: {
    type: Boolean,
    default: false
  },
  expireAt: {
    type: Date,
    default: undefined
  }
})

var Streamer = module.exports = mongoose.model('Streamer', streamerSchema)

module.exports.getAllStreams = async function () {
  var streamerPool = await new Promise(function (resolve, reject) {
    Streamer.find(function (err, streamers) {
      if (err)reject()
      resolve(streamers)
    })
  }).catch(error => { console.log('caught', error) })
  if (streamerPool == undefined) return []
  return streamerPool.reverse()
}
module.exports.isAstreamer = async function (socketID) {
  var result = await new Promise(function (resolve, reject) {
    Streamer.find({socketID: socketID}, function (err, result) {
      if (err)reject()
      resolve(result)
    })
  }).catch(error => { console.log('caught', error) })
  return result.length >= 1
}
module.exports.removeStreamerFromSocketId = async function (socketID) {
  Streamer.deleteOne({socketID: socketID}, function (err) {
    if (err) throw (err)
    console.log('1 document deleted')
  })
}
module.exports.getStreamFromSocketID = async function (socketID) {
  var result = await new Promise(function (resolve, reject) {
    var result = Streamer.find({socketID: socketID}, function (err, result) {
      if (err) reject()
      resolve(result)
    })
  })
  return result
}
module.exports.existStreamWithSessionID = async function (sessionID) {
  var result = await new Promise(function (resolve, reject) {
    Streamer.find({sessionID: sessionID}, function (err, result) {
      if (err) reject()
      resolve(result)
    })
  })
  return result.length >= 1
}

module.exports.getStreamers = async function () {
  var result = await new Promise(function (resolve, reject) {
    Streamer.find(function (err, result) {
      if (err)reject()
      resolve(result)
    })
  }).catch(error => { console.log('caught', error) })
  if (result == undefined) return []
  return result.reverse()
}
module.exports.addSocketID = async function (sessionID, socketID) {
  var currentStream = {sessionID: sessionID}
  var updatedStream = {socketID: socketID}
  var result = await new Promise(function (resolve, reject) {
    Streamer.findOneAndUpdate(currentStream, updatedStream, function (err) {
  	   if (err) reject()
      console.log('1 document updated')
      resolve(result)
    })
  }).catch(error => { console.log('caught', error) })
  return result
}
