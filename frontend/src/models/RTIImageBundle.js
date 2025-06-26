/**
 * Represents a relightable RTI image in the ["relight-web"](https://vcg.isti.cnr.it/vcgtools/relight/#format) format.
 * 
 * This bundle includes all necessary files to view or process the RTI,
 * such as an `info.json` file, multiple JPEG planes, and a thumbnail.
 */
export default class RTIImageBundle {
    /** @type {string} */
    id
    /** @type {HttpUrl} */
    url
    /** @type {HttpUrl} */
    thumbnail
    /** @type {string[]} */
    filenames

    /** From raw json data */
    constructor(data) {
        this.id = typeof data.id === 'string' ? data.id : ''
        this.url = typeof data.url === 'string' ? data.url : ''
        this.thumbnail = typeof data.thumbnail === 'string' ? data.thumbnail : null
        this.filenames = Array.isArray(data.filenames) ? data.filenames.map(name => String(name)) : []
    }
}
