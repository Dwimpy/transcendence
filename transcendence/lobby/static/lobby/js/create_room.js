addEventListener("DOMContentLoaded", load_room_modal)




function load_room_modal() {

    const modalDialog = document.getElementById("dialog")
    const create_room = document.getElementById("create_room_button")

    create_room.addEventListener("click", function () {
        fetch("http://127.0.0.1:8000/lobby/create_room/")
        .then(html => html.text())
        .then(text => {
            modalDialog.innerHTML = text;
            })
        }
    )
}
