import { Metadata } from "./metadata";

/**
* @typedef {Object} ArtifactParams
* @property {string} id
* @property {MetadataParams} metadata
* @property {string[]} images
* @property {*} rtis //TODO: make typedef for webrtis
*/
class Artifact {
    /**
     * @param {ArtifactParams} params 
     */
    constructor({
        id = '',
        metadata = new Metadata(),
        images = [],
        rtis = { web: [] },
    } = {}) {
        this.id = id;
        this.metadata = metadata;

        // media
        this.thumbnail = metadata?.thumbnail;
        this.images = images;
        this.RTIs = rtis?.web;
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