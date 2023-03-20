const socket = new WebSocket(`wss://${window.location.host}/dir/`)
console.log(socket)
console.log(window.location.href)
socket.onmessage = function(e) {
    const message = JSON.parse(e.data)
    console.log(message)
}