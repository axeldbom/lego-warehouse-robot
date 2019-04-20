var express = require('express')
var router = express.Router()
var Streamer = require('../models/stream')

router.get('/', function (req, res) {
  res.render('streamers/stream')
  // req.io.on('connection', function (socket) {
  //   // DO something
  // })
})

router.post('/:streamID', async function (req, res) {
  var nickname = req.body.nickname
  var title = req.body.title
  var robotClient = req.body.robotClient
  var password = '0000' // use a lib for generating passwords
  var streamID = req.params.streamID
  let socket_id = []

  req.io.on('connection', async function (socket) {
    socket_id.push(socket.id)
    if (socket_id[0] === socket.id) {
      req.io.removeAllListeners('connection')
    }
    socket.on('streamSocket', async function () {
      if (!req.session.createStreamLock) {
        if (!(await Streamer.isAstreamer(socket.id))) {
          console.log('in streamers/:stremID')
          var newStreamer = new Streamer({
            title: title,
            name: nickname,
            controlPassword: password,
            socketID: socket.id,
            sessionID: req.sessionID
          })
          if (robotClient) {
            newStreamer.robotClient = robotClient
          }
          newStreamer.save(function (err) {
            if (err) {
              console.log(err) // TODO:  Fix 11000 duplicate key error
            }
          })
          socket.join(socket.io)
          socket.broadcast.emit('newStreamCreated', newStreamer)
        }
        req.session.createStreamLock = true
      }
    })
  })
  res.redirect('/streamers')
})

module.exports = router
