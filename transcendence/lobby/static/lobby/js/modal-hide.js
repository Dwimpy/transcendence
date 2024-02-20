
if (window.location.pathname === '/lobby/') {
    addEventListener("DOMContentLoaded", hide_modal)
}

function hide_modal() {
    const modal = new bootstrap.Modal(document.getElementById("create_room_modal"))

    htmx.on("htmx:afterSwap", (e) => {
    if (e.detail.target.id === "dialog") {
        modal.show();
    }
})

    htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
        modal.hide();
        e.detail.shouldSwap = false;
    }
})


    htmx.on("htmx:wsAfterMessage", (e) => {
        if (e.detail.elt.id === 'create_room_modal') {
            const received_data = e.detail.message;
            const div = document.createElement('div');
            div.innerHTML = received_data;
            const errorElement = div.querySelector('#errors');
            if (!errorElement)
               modal.hide();
        }
})

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = "";
})
}
