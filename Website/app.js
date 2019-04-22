const express = require('express')
const path = require('path')
var flash = require('connect-flash')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const exphbs = require('express-handlebars')
const session = require('express-session')
const Handlebars = require('handlebars')

// db stuff
var mongo = require('mongodb')
var mongoose = require('mongoose')
var MongoStore = require('connect-mongo')(session)

// Handlebars help func start

mongoose.connect('mongodb://localhost/loginapp', {
  useNewUrlParser: true,
  useCreateIndex: true
}).catch(function (error) {
  console.log(' ----------------------------------------------')
  console.log(' Make sure to start a mongodb server instance!!')
  console.log(' exiting...')
  console.log(' ----------------------------------------------')
  process.exit()
})
var db = mongoose.connection

// Init App
var app = express()

 // mongodb models
var Streamer = require('./models/stream')

  // View Engine
app.set('views', path.join(__dirname, 'views'))
app.engine('handlebars', exphbs({defaultLayout: 'layout'}))
app.set('view engine', 'handlebars')

  // BodyParser Middleware
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

  // Set Static Folder
app.use(express.static(path.join(__dirname, 'public')))

// Connect Flash
app.use(flash())

  // Express Session
app.use(session({
  secret: 'secret',
  store: new MongoStore({ mongooseConnection: mongoose.connection}),
  saveUninitialized: true,
  resave: true,
  cookie: { maxAge: 3600000 }
}))

/* Socket.io stuff */
var server = require('http').Server(app)
var io = require('socket.io')(server)

// Global Vars
app.use(async function (req, res, next) {
  res.locals.success_msg = req.flash('success_msg')
  res.locals.error_msg = req.flash('error_msg')
  res.locals.error = req.flash('error')
  req.io = io // Making the socket obj "io" global middleware
  req.streamers = {}
  next()
})
var controlledStreams = {}
io.on('connection', async function (socket) {
  console.log('socket connected ' + socket.id)

  socket.on('disconnect', async function () {
    console.log('socket disconnected ' + socket.id)
    if (await Streamer.isAstreamer(socket.id)) {
      socket.broadcast.emit('removedStreamer', socket.id)
      delete controlledStreams[socket.id]
      await Streamer.removeStreamerFromSocketId(socket.id)
    }
  })

  socket.on('forwardImage', function (image) {
    socket.to(socket.id).emit('forwardImage', image)
  })
  socket.on('forwardImageRobot', function (image) {
    image = image.substring(2, image.length - 1)
    socket.to(socket.id).emit('forwardImageRobot', image)
  })
  socket.on('startNewStream', async function (sessionID) {
    var newStreamer = await Streamer.addSocketID(sessionID, socket.id)
    socket.broadcast.emit('newStreamCreated', newStreamer)
  })
  socket.on('observerSocket', function (socketID) {
    socket.join(socketID)
    console.log('Socket: ' + socket.id + ' joins the group of socket: ' + socketID)
  })
  socket.on('startNewStreamRobot', async function (data) {
    // console.log(data)
    var newStreamer = new Streamer({
      title: data.title,
      name: data.nickname,
      controlPassword: data.password,
      sessionID: 'Robot - no ID',
      socketID: socket.id,
      robotClient: data.robotClient
    })
    console.log('--------------------')
    console.log(newStreamer.socketID)
    console.log('--------------------')
    newStreamer.save(function (err) {
      if (err) {
        console.log(err) // TODO:  Fix 11000 duplicate key error
      }
    })
    controlledStreams[socket.id] = false
    socket.broadcast.emit('newStreamCreated', newStreamer)
  })
  socket.on('gainControlOfTheRobot', function (streamerID, callback) {
    if (!controlledStreams[streamerID]) {
      controlledStreams[streamerID] = true
      socket.in(streamerID).emit('lockControlButton')
      callback(true)
    } else {
      callback(false)
    }
  })
  socket.on('releaseRobotButton', function (streamerID) {
    if (controlledStreams[streamerID]) {
      controlledStreams[streamerID] = false
      socket.in(streamerID).emit('unlockControlButton')
    }
  })
  socket.on('controlRobot', function (obj) {
    if (controlledStreams[obj.streamerID]) {
      io.to(`${obj.streamerID}`).emit('keys', obj.keys)
    }
  })
})
var routes = require('./routes/index')
var streamers = require('./routes/streamers')
var observers = require('./routes/observers')

app.use('/', routes)
app.use('/streamers', streamers)
app.use('/observers', observers)

// Set Port
app.set('port', (process.env.PORT || 3000))

server.listen(app.get('port'), function () {
  console.log('Server started on port ' + app.get('port'))
})
