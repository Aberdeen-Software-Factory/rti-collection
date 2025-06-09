async function autodetect() {
	let response = await fetch('plane_0.tzi');
	if(response.status == 200)
		return "tarzoom";

	response = await fetch('plane_0.dzi');
	if(response.status == 200)
		return "deepzoom";

        response = await fetch('planes.tzi');
        if(response.status == 200)
                return "itarzoom";

	response = await fetch('plane_0.jpg');
	if(response.status == 200)
                return "image";

	alert("Could not detect an RTI here");
	return "";
}

async function autodetectNormals(layout) {
	if(layout == 'tarzoom') {
		let response = await fetch('normals.tzi');
		if(response.status == 200)
			return true;
	}
	if(layout == 'deepzoom') {
		let response = await fetch('normals.dzi');
		if(response.status == 200)
			return true;
	}
	if(layout == 'image') {
		let response = await fetch('normals.jpg');
		if(response.status == 200)
			return true;
	}

	return false;
}