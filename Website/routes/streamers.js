var express = require('express')
var router = express.Router()
var Streamer = require('../models/stream')

router.get('/', async function (req, res) {
  if (await Streamer.existStreamWithSessionID(req.sessionID)) {
    res.render('streamers/stream')
  } else {
    req.flash('error_msg', 'To start streaming, create an entry below')
    res.redirect('/')
  }
})

router.post('/p/:streamID', async function (req, res) {
  var nickname = req.body.nickname
  var title = req.body.title
  var robotClient = req.body.robotClient
  var password = '0000' // use a lib for generating passwords

  console.log('in streamers/:streamID')
  var newStreamer = new Streamer({
    title: title,
    name: nickname,
    controlPassword: password,
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

  res.redirect('/streamers?s=' + req.sessionID)
})
module.exports = router
