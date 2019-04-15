var express = require('express')
var path = require('path')
var cookieParser = require('cookie-parser')
var bodyParser = require('body-parser')
var exphbs = require('express-handlebars')
var session = require('express-session')
var Handlebars = require('handlebars')

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
var Stremer = require('./models/stream')

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
  req.io = io // Making the socket obj "io" global middleware
  req.streamers = {}
  next()
})

io.on('connection', function (socket) {
  console.log('socket connected ' + socket.id)

  socket.on('disconnect', async function () {
    console.log('socket disconnected ' + socket.id)
    if (await Stremer.isAstreamer(socket.id)) {
      socket.broadcast.emit('removedStreamer', socket.id)
      await Stremer.removeStreamerFromSocketId(socket.id)
    }
  })

  socket.on('forwardImage', function (image) {
    // socket.broadcast.emit('forwardImage', image)
    socket.to(socket.id).emit('forwardImage', image)
    // console.log(image)
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
