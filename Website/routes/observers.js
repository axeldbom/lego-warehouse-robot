var express = require('express')
var router = express.Router()
var Streamer = require('../models/stream')

router.get('/:streamID', async function (req, res) {
  var streamID = req.params.streamID
  const streamerInfo = await Streamer.getStreamFromSocketID(streamID)
  if (streamerInfo.length < 1) {
    req.flash('error_msg', 'Streamer not found, please try with an entry from the list below')
    res.redirect('/') // add message
    return
  }
  let socket_id = []
  req.io.on('connection', function (socket) {
    socket_id.push(socket.id)
    if (socket_id[0] === socket.id) {
      req.io.removeAllListeners('connection')
    }
    socket.on('observerSocket', function (socketID) {
      if (!req.session.joinStreamLock) {
        socket.join(socketID)
        console.log('Socket: ' + socket.id + ' joins the group of socket: ' + socketID)
        req.session.joinStreamLock = true
      }
    })
  })
  res.render('observers/stream', {streamerInfo: streamerInfo[0]})
})

module.exports = router
