import Metadata from "@/models/Metadata"
import RTIImageBundle from "@/models/RTIImageBundle"

/**
 * Represents an artifact record with metadata, still images, and RTI image bundles.
 */
export default class Artifact {
    /** @type {string} */
    id
    
    /** @type {Metadata} */
    metadata

    /** 
     * List of URLs to still images of the artifact.
     * @type {HttpUrl[]}
     */
    images

    /** 
     * List of objects that each describe a relightable image bundle.
     * @type {RTIImageBundle[]}
     */
    rtis

    constructor(data = {}) {
        this.id = typeof data.id === 'string' ? data.id : ''
        this.metadata = new Metadata(data.metadata || {})
        this.images = Array.isArray(data.images) ? data.images.map(imgSrc => String(imgSrc)) : []
        this.rtis = Array.isArray(data.rtis) ? data.rtis.map(r => new RTIImageBundle(r)) : []
    }

    get defaultMedia() {
        return this.rtis?.[0]?.url || this.images?.[0] || ''
    }
}
