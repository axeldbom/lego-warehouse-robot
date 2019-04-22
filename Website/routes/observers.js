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
  res.render('observers/stream', {streamerInfo: streamerInfo[0]})
})

module.exports = router
