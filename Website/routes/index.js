var express = require('express')
var router = express.Router()
var Stream = require('../models/stream')

// Get Homepage
router.get('/', async function (req, res) {
  let allStreams = await Stream.getAllStreams()
  res.render('main', {streamers: allStreams, sessionID: req.sessionID})
  // console.log(req.session.cookie)
})

module.exports = router
