const canvas = document.getElementById('PongCanvas'); // Assuming 'PongCanvas' is the correct selector
const context = canvas.getContext('2d');

function drawPaddles() {  // Corrected function name
    context.fillStyle = '#fff';
    context.fillRect(0, 100, 20, 100);
}

console.log(canvas)

drawPaddles()

