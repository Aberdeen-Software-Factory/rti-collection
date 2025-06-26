import Metadata from "@/models/Metadata";

/**
 * A simpler representation of an artifact, used in lists.
 */
export default class ArtifactPreview {
    /** @type {string} */
    id

    /** @type {Metadata} */
    metadata

    /** @type {HttpUrl} */
    thumbnail

    constructor(data = {}) {
        this.id = String(data.id || '');
        this.metadata = new Metadata(data.metadata || {});
        this.thumbnail = String(data.thumbnailURL || '');
    }
}