let socketIdLength = 20
var streamerID = document.URL.substring(document.URL.length, document.URL.length - socketIdLength)
socket.emit('observerSocket', streamerID)
socket.on('forwardImage', function (image) {
  const img = document.getElementById('cameraImg')
  img.src = 'data:image/jpeg;base64,' + image + ''
})
