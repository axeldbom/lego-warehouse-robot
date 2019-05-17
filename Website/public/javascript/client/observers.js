let socketIdLength = 20
var streamerID = document.URL.substring(document.URL.length, document.URL.length - socketIdLength)
var controller = false // not safe but should work
socket.emit('observerSocket', streamerID)
console.log(socket.id)
console.log('observerSocket')

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
  return (key == 'ArrowUp' || key == 'ArrowDown' || key == 'ArrowLeft' || key == 'ArrowRight' || key == ' ' || key == 'a')
}

function keyHandler (bool, key) {
  if (key == ' ') {
    keys.SpaceBar = bool
  } else {
    keys[key] = bool
  }
}
var lock = true

const keys = {
  ArrowUp: false,
  ArrowDown: false,
  ArrowLeft: false,
  ArrowRight: false,
  SpaceBar: false,
  a: false
}
function onKeyDown (event) {
  if (!keysOfInterest(event.key)) return
  keyHandler(true, event.key)
  if (controller) {
    let obj = {
      streamerID: streamerID,
      keys: keys
    }
    if (lock) {
      lock = false
      socket.emit('controlRobot', obj)
      setTimeout(function () {
        lock = true
      }, 40)
    }
  }
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

// control robot stuff start
function gainControlOfTheRobot () {
  if (document.getElementById('controlRobotButton')) {
    document.getElementById('controlRobotButton').onclick = function (event) {
      socket.emit('gainControlOfTheRobot', streamerID, function (answer) {
        if (answer) {
          controller = true
          document.getElementById('controlRobotButton').style.display = 'none'
          document.getElementById('releaseRobotButton').style.display = 'block'
        }
      })
    }
  }
}
socket.emit('newRobotObserver', streamerID, function (answer) {
  if (answer) {
    document.getElementById('controlRobotButton').disabled = true
  }
})
function releaseControlOfTheRobot () {
  if (document.getElementById('releaseRobotButton')) {
    document.getElementById('releaseRobotButton').onclick = function (event) {
      socket.emit('releaseRobotButton', streamerID)
      controller = false
      document.getElementById('controlRobotButton').style.display = 'block'
      document.getElementById('releaseRobotButton').style.display = 'none'
    }
  }
}

gainControlOfTheRobot()
releaseControlOfTheRobot()

socket.on('lockControlButton', function () {
  document.getElementById('controlRobotButton').disabled = true
})
socket.on('unlockControlButton', function () {
  document.getElementById('controlRobotButton').disabled = false
})
// control robot stuff end
