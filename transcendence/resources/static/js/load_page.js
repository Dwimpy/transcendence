document.addEventListener('DOMContentLoaded', function () {
        function load_page(url) {
            let request = new XMLHttpRequest();
            request.open('GET', url, true);

            request.onreadystatechange = function () {
                if (request.DONE && request.status === 200) {
                    document.getElementById("main-content").innerHTML = request.responseText;
                } else if (request.DONE && request.status === 404) {
                    console.log("Failed to load template")
                }
            };
            request.send()
        }
        load_page('/lobby/game_lobby')

    document.body.addEventListener('click', function(event) {
        if (event.target && event.target.id === 'create-room-content') {
            load_page('/lobby/create_room');
        }
    });

    document.body.addEventListener('click', function(event) {
        if (event.target && event.target.id === 'btn-back-to-lobby') {
            load_page('/lobby/game_lobby');
        }
    });

    }
);


// document.addEventListener('DOMContentLoaded', function () {
//     // Function to load the create room template
//     function loadCreateRoom() {
//         var xhr = new XMLHttpRequest();
//         xhr.open('GET', '/create_room/', true);
//
//         xhr.onreadystatechange = function () {
//             if (xhr.readyState == 4 && xhr.status == 200) {
//                 // Update the create room container with the fetched template
//                 document.getElementById('create-room-container').innerHTML = xhr.responseText;
//             } else if (xhr.readyState == 4 && xhr.status != 200) {
//                 console.error('Failed to load create room template.');
//             }
//         };
//
//         xhr.send();
//     }
//
//     // Bind the load function to the button click event
//     document.getElementById('load-create-room-button').addEventListener('click', function () {
//         loadCreateRoom();
//     });
// });