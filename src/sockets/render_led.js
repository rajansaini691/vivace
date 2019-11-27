/*
 * Converts RGB values stored as integers to a hex string quickly
 * (see https://gist.github.com/lrvick/2080648)
 */
function rgbToHex(r,g,b) {
    var bin = r << 16 | g << 8 | b;
    return "#" + (function(h){
        return new Array(7-h.length).join("0")+h
    })(bin.toString(16).toUpperCase())
}

/*
 * Renders the given rgb pixel values to a canvas
 * 
 * @param ctx		The context of the canvas that we draw to
 * @param pixels	An array of rgb color values that map to the pixels on
 *			an LED strip. For example, [0,0,0,255,255,255] maps to
 *			BLACK, WHITE
 */
function renderLEDStrip(ctx, pixels) {
	if(!pixels || pixels.length < 3) return;

	// Draw multiple LEDs
	for(var i = 0; i < pixels.length; i += 3) {
		var r = pixels[i];
		var g = pixels[i+1];
		var b = pixels[i+2];

		ctx.beginPath();
		ctx.rect(20, 20, 150, 100);
		ctx.fillStyle = rgbToHex(r, g, b);
		ctx.fill();
	}

}

function startSocket() {
	// Opens a websocket
	var ws_addr = "ws://" + location.hostname + ":4444";
	var ws = new WebSocket(ws_addr);

	var canvas = document.getElementById("led_renderer");
	var ctx = canvas.getContext("2d");

	ctx.beginPath();
	ctx.rect(20, 20, 150, 100);
	ctx.fillStyle = "red";
	ctx.fill();

	ws.onmessage = function (evt) { 
		// Convert bytes to int array
		var BYTES_PER_INT = 1;

		const fr = new FileReader();
		fr.readAsArrayBuffer(evt.data);
		fr.onload = () => {
			// Stores the rgb pixel values
			var pixels = [];

			const data = new Uint8Array(fr.result);

			for(var i = 0; i < data.length / BYTES_PER_INT; i += 1) {
				pixels.push(0);
				for(var j = 0; j < BYTES_PER_INT; j++) {
					pixels[i] <<= 8;
					pixels[i] |= data[i * BYTES_PER_INT + j];
				}
				
			}

			renderLEDStrip(ctx, pixels);
		}

	};
	
	ws.onclose = function() { 
	  // websocket is closed.
	  alert("Connection is closed..."); 
	};
}

