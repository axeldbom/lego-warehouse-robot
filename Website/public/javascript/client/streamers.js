let idLength = 32
var userID = document.URL.substring(document.URL.length, document.URL.length - idLength)
socket.emit('startNewStream', userID)
Webcam.set({
  width: 600,
  height: 400,
  image_format: 'jpeg',
  jpeg_quality: 90,
  flip_horiz: true
})

Webcam.attach('mywebcam')// https://github.com/jhuckaby/webcamjs
function useCamera () {
  var no = 60
  var FPS = 1000 / no
  Webcam.on('load', function () {
    setInterval(function () {
      Webcam.snap(function (data_uri) {
        var raw_image_data = data_uri.replace(/^data\:image\/\w+\;base64\,/, '')
        socket.emit('forwardImage', raw_image_data)
      })
    }, FPS)
  })
}

useCamera()

// socket.on('disconnect', function () {
//   console.log('Hello')
// })

console.log(socket.id)
