var express = require('express')
var router = express.Router()
var Stremer = require('../models/stream')

router.get('/', function (req, res) {
  res.render('streamers/stream')
  // req.io.on('connection', function (socket) {
  //   // DO something
  // })
})

router.post('/:streamID', async function (req, res) {
  var nickname = req.body.nickname
  var title = req.body.title
  var password = '0000' // use a lib for generating passwords
  var streamID = req.params.streamID
  console.log(nickname)
  console.log(title)

  req.io.on('connection', async function (socket) {
    socket.on('streamSocket', async function () {
      if (!req.session.createStreamLock) {
        if (!(await Stremer.isAstreamer(socket.id))) {
          console.log('in streamers/:stremID')
          var newStreamer = new Stremer({
            title: title,
            name: nickname,
            controlPassword: password,
            socketID: socket.id,
            sessionID: req.sessionID
          })
          newStreamer.save(function (err) {
            if (err) {
              console.log(err) // TODO:  Fix 11000 duplicate key error
            }
          })
          socket.join(socket.io)
          socket.broadcast.emit('newStreamCreated', newStreamer)
        // req.session.cookie.streamInfo[socketID] = true // TODO: make this scope run once, part 1
        }
        req.session.createStreamLock = true
      }
    })
  })
  res.redirect('/streamers')
})

router.post('/r/o', async function (req, res) {
  console.log('HELLO')
  res.redirect('/')
})

module.exports = router
