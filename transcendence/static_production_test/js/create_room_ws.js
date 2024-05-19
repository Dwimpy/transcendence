const lobby_socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/create_room')

lobby_socket.onmessage = function(event) {

    const data = JSON.parse(event.data)

    console.log(data.message)

}