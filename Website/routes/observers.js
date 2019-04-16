var express = require('express')
var router = express.Router()

router.get('/:streamID', function (req, res) {
  var streamID = req.params.streamID
  req.io.on('connection', function (socket) {
    socket.on('observerSocket', function (socketID) {
      if (!req.session.joinStreamLock) {
        socket.join(socketID)
        console.log('Socket: ' + socket.id + ' joins the group of socket: ' + socketID)
        req.session.joinStreamLock = true
      }
    })
  })
  res.render('observers/stream')
})

module.exports = router
