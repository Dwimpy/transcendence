

const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/')


socket.onopen = function (event) {
    console.log("Client connected", event)
    socket.send(JSON.stringify({"message": 'what the fuck'}))
}

socket.onmessage = function (event) {
    const data = JSON.parse(event.data)
    console.log("Message received:  " + data)
}

socket.onclose = function (event) {
    console.log("Awww, you're leaving already ?")
}

