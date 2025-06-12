class Artifact {
    constructor({ id, title, description, creator, date, thumbnail, images, relightableMedia }) {
        // metadata
        this.id = id;
        this.title = title;
        this.description = description;
        this.creator = creator;
        this.date = date;
        // media
        this.thumbnail = thumbnail;
        this.images = images;
        this.RTIs = relightableMedia;
    }
}

class ArtifactPreview {
    constructor({ id, title, date, num_images, num_rtis, thumbnail }) {
        this.id = id;
        this.title = title;
        this.date = date;
        this.imageCount = num_images;
        this.RTICount = num_rtis;
        this.thumbnail = thumbnail;
    }
}

export { Artifact, ArtifactPreview }