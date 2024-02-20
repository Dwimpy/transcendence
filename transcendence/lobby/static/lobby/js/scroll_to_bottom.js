
htmx.on('htmx:wsAfterSend', (event) => {
    console.log(event.detail.elt.id);
    if (event.detail.elt.id === 'create_room_modal') {
            const table = document.getElementById('room_table');
            table.scrollTo({
                top: table.scrollHeight,
                behavior: 'smooth' // You can use 'auto' for immediate scrolling
            });
    }
});