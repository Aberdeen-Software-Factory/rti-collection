function initRTI(viewer, path) {
    // let layout = await autodetect(path);
    // let normals = await autodetectNormals(layout, path);
    let layout = 'image';
    let normals = false;

    var lime = new OpenLIME.Viewer(viewer, {
        background: 'black'
    });
    
    let layer = new OpenLIME.Layer({
        type:'rti',
        url: path,
        layout: layout, 
        normals: normals
    });
    
    lime.canvas.addLayer('RTI', layer); 
    OpenLIME.Skin.setUrl('openlime/skin.svg');
    let ui = new OpenLIME.UIBasic(lime, {
        // skin: 'skin.svg',
        showLightDirections: false
    });
    // ui.actions.light.active = true;
    ui.toggleLightController(true);

    // ui.actions.layers.display = true;
    lime.camera.maxFixedZoom = 1;
    window.lime = lime;

    return [lime, ui]
}

function initJPG(viewer, path) {
    let layout = 'image';
    let normals = false;

    var lime = new OpenLIME.Viewer(viewer, {
        background: 'black'
    });
    
    let layer = new OpenLIME.LayerImage({
        id: 'base-image',
        layout: 'image',
        url: path,
    });
			
    lime.canvas.addLayer('JPG', layer);

    let ui = new OpenLIME.UIBasic(lime);
    ui.actions.light.display = false;
    ui.actions.layers.display = false;

    // ui.actions.layers.display = true;
    lime.camera.maxFixedZoom = 1;
    window.lime = lime;

    return [lime, ui]
}

export { initRTI, initJPG }