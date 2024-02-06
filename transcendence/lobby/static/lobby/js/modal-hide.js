
addEventListener("DOMContentLoaded", hide_modal)

function hide_modal() {
    const modal = new bootstrap.Modal(document.getElementById("create_room_modal"))

    htmx.on("htmx:afterSwap", (e) => {
    if (e.detail.target.id === "dialog") {
        modal.show()
    }
})

    htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
        modal.hide()
        e.detail.shouldSwap = false
    }
})

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
})
}
