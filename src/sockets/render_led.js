window.onload = function() {
	// Opens a web socket at port 4444
	var ws_addr = "ws://" + location.hostname + ":4444";
	var ws = new WebSocket(ws_addr);
	console.log("TEST");

	/*
	 * Called whenever the server pushes data
	 */
	ws.onmessage = function (evt) { 
		// Stores the rgb array being rendered
		var pixels = [];

		// Stores initial binary data coming from server
		var arr = evt.data;

		/*
		 * Convert socket data to an array
		 */
		const fr = new FileReader();
		fr.readAsArrayBuffer(arr);

		// The incoming data format
		var BYTES_PER_INT = 1;

		fr.onload = () => {
			const data = new Uint8Array(fr.result);

			for(var i = 0; i < data.length / BYTES_PER_INT; i += 1) {
				pixels.push(0);

				for(var j = 0; j < BYTES_PER_INT; j++) {
					pixels[i] <<= 8;
					pixels[i] |= data[i * BYTES_PER_INT + j];
				}
			}
		}
		console.log("TEST");
		console.log(pixels);
	};
}
