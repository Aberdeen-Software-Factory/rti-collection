class Artifact {
    constructor({ id, title, description, creator, date, thumbnail, imageURLs, RTIs }) {
        // metadata
        this.id = id;
        this.title = title;
        this.description = description;
        this.creator = creator;
        this.date = date;
        // media
        this.thumbnail = thumbnail;
        this.images = imageURLs;
        this.RTIs = RTIs;
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