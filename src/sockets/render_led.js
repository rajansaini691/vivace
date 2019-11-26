function render() {
	// Init
	var c = document.getElementById("led_renderer");
	var ctx = c.getContext("2d");

	// Draw a single LED
	ctx.beginPath();
	ctx.rect(20, 20, 150, 100);
	ctx.stroke();
}

function WebSocketTest() {
	// Opens a websocket
	var ws_addr = "ws://" + location.hostname + ":4444";
	var ws = new WebSocket(ws_addr);

	ws.onmessage = function (evt) { 
		var arr = evt.data;

		// TODO Get this value from configuration
		var BYTES_PER_INT = 1;

		// Convert bytes to int array
		const fr = new FileReader();
		fr.readAsArrayBuffer(arr);
		fr.onload = () => {
		const data = new Uint8Array(fr.result);

		var pixels = [];
		for(var i = 0; i < data.length / BYTES_PER_INT; i += 1) {
			pixels.push(0);
			for(var j = 0; j < BYTES_PER_INT; j++) {
				pixels[i] <<= 8;
				pixels[i] |= data[i * BYTES_PER_INT + j];
			}
			
		}
		console.log(pixels);
		}
	};
	
	ws.onclose = function() { 
	  // websocket is closed.
	  alert("Connection is closed..."); 
	};
}

