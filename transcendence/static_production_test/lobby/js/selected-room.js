

addEventListener("DOMContentLoaded", select_room)


function select_room() {
    // Delegate the click event to the tbody element (or a parent element that doesn't get replaced)
    const table = document.querySelector('table');
    table.addEventListener('click', function(event) {
        const target = event.target;
        // Check if the clicked element is a tr inside the tbody
            targettr = target.closest('tr')
        if (targettr && targettr.tagName === 'TR') {
            // Remove 'table-active' class from all tr elements
            table.querySelectorAll('tr').forEach(function(innerItem) {
                innerItem.classList.remove('table-active');
            });

            // Add 'table-active' class to the clicked tr element
            targettr.classList.add('table-active');
        }
    });
}

