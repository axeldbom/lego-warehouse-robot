var streamerHolder = {}
socket.on('newStreamCreated', function (streamInfo) {
  // var socketID = streamInfo.socketID
  // if (streamerHolder.socketID == undefined) {
  //   streamerHolder.socketID = true
  //   console.log(streamInfo)
  //   createStreamEntry(streamInfo)
  // }
})
socket.on('removedStreamer', function (streamID) {
  deleteStreamEntry(streamID)
})

document.getElementById('streamButton').onclick = function () {
  document.getElementById('overlayDiv').style.display = 'block'
}

function createStreamEntry (streamInfo) {
  let listOfstreamers = document.getElementById('ListOfstreamers')

  let outerDiv = document.createElement('DIV')
  outerDiv.setAttribute('class', 'list-group')
  outerDiv.setAttribute('id', streamInfo.socketID)
  listOfstreamers.prepend(outerDiv)

  let aTag = document.createElement('a')
  aTag.setAttribute('class', 'list-group-item list-group-item-action flex-column align-items-start')
  aTag.setAttribute('href', '/observers/' + streamInfo.socketID)
  outerDiv.appendChild(aTag)

  let innerDiv = document.createElement('DIV')
  innerDiv.setAttribute('class', 'd-flex w-100 justify-content-between')
  aTag.appendChild(innerDiv)

  let h5 = document.createElement('H5')
  h5.setAttribute('class', 'mb-1')
  h5.innerHTML = streamInfo.title
  innerDiv.appendChild(h5)

  let small1 = document.createElement('SMALL')
  small1.innerHTML = 'Status: online'
  innerDiv.appendChild(small1)

  let pTag = document.createElement('P')
  pTag.setAttribute('class', 'mb-1')
  pTag.innerHTML = 'Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.'
  aTag.appendChild(pTag)

  let small2 = document.createElement('SMALL')
  small1.innerHTML = 'Streamer: ' + streamInfo.name
  aTag.appendChild(small2)
}
function deleteStreamEntry (streamID) {
  if (document.getElementById(streamID) != undefined) {
    document.getElementById(streamID).remove()
    // document.getElementById(streamID).style.display = 'none'
  }
}
