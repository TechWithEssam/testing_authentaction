const RoomNameInput = document.querySelector('#room-name-input').focus()
    const slug = document.getElementById("slug").textContent.trim()
    const roomName = JSON.parse(document.getElementById('room-slug').textContent);
    
    const url = `ws://${window.location.host}/ws/dir/${slug}/`
    console.log(url)
    
    const chatSocket = new WebSocket(url);