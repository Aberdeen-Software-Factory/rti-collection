class Artifact {
    constructor({ id, metadata, images, rtis }) {
        // metadata
        this.id = id;
        this.title = metadata.title;
        this.description = metadata.description;
        this.creator = metadata.creator;
        this.date = metadata.date;
        // media
        this.thumbnail = metadata.thumbnail;
        this.images = images;
        this.RTIs = rtis.web;
    }
}

class ArtifactPreview {
    constructor({ id, title, date, num_images, num_rtis, thumbnailURL }) {
        this.id = id;
        this.title = title;
        this.date = date;
        this.imageCount = num_images;
        this.RTICount = num_rtis;
        this.thumbnailURL = thumbnailURL;
    }
}

export { Artifact, ArtifactPreview }