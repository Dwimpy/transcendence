document.addEventListener('DOMContentLoaded', function() {
    let roomItems = document.querySelectorAll('.lobby-item')

    roomItems.forEach(function (item){
        item.addEventListener('click', function() {
            roomItems.forEach(function(innerItem) {
               innerItem.classList.remove('selected')
            });

            item.classList.add('selected')
        });
    });
});