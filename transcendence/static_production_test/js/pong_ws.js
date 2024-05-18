
const pong_socket = new WebSocket('ws://' + window.location.host + '/ws/pong/')


pong_socket.onopen = function (event) {
    console.log("Client connected", event)
    pong_socket.send(JSON.stringify({"message": 'what the fuck'}))
}

pong_socket.onmessage = function (event) {
    const data = JSON.parse(event.data)
    console.log("Message received:  " + data)
}

pong_socket.onclose = function (event) {
    console.log("Awww, you're leaving already ?")
}