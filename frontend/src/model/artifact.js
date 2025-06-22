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

/**
* @typedef {Object} ArtifactPreviewParams
* @property {string} id
* @property {MetadataParams} metadata
* @property {string} thumbnailURL
*/
class ArtifactPreview {
    /**
     * @param {ArtifactPreviewParams} params 
     */
    constructor({ id, metadata, thumbnailURL }) {
        this.id = id;
        this.metadata = metadata;
        this.thumbnailURL = thumbnailURL;
    }
}

export { Artifact, ArtifactPreview }