var lock = false
let socketIdLength = 20
var streamerID = document.URL.substring(document.URL.length, document.URL.length - socketIdLength)
if (!lock) {
  lock = true
  socket.emit('observerSocket', streamerID)
}
socket.on('forwardImage', function (image) {
  const img = document.getElementById('cameraImg')
  img.src = 'data:image/jpeg;base64,' + image + ''
})
socket.on('forwardImageRobot', function (image) {
  const img = document.getElementById('cameraImg')
  img.src = 'data:image/jpeg;base64,' + image
})

// Key press functionality start
function keysOfInterest (key) {
  return (key == 'ArrowUp' || key == 'ArrowDown' || key == 'ArrowLeft' || key == 'ArrowRight' || key == ' ')
}

function keyHandler (bool, key) {
  if (key == ' ') {
    keys.SpaceBar = bool
  } else {
    keys[key] = bool
  }
}

const keys = {
  ArrowUp: false,
  ArrowDown: false,
  ArrowLeft: false,
  ArrowRight: false,
  SpaceBar: false
}
function onKeyDown (event) {
  if (!keysOfInterest(event.key)) return
  keyHandler(true, event.key)
  console.log(keys)
}
function onKeyUp (event) {
  // if (event.key == 'Enter') {
  //   console.log('not implemented')
  // }
  if (!keysOfInterest(event.key)) return
  keyHandler(false, event.key)
}

document.onkeydown = onKeyDown
document.onkeyup = onKeyUp
// Key press functionality end

document.getElementById('controlRobotButton').onclick = function (event) {
  console.log('HELLO')
}
