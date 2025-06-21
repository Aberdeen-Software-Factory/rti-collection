/**
* @typedef {Object} MetadataParams
* @property {string} name
* @property {string[]} language
* @property {string[]} script
* @property {string[]} provenance
* @property {string[]} location
* @property {string[]} photographer
* @property {string} date
* @property {string} bibliography
* @property {string} notes
* @property {string[]} keywords
* @property {string} copyright
*/

/**
 * Represents metadata for an artifact.
 */
class Metadata {
    /**
    * @param {MetadataParams} params
    */
    constructor({
        name = '',
        language = [],
        script = [],
        provenance = [],
        location = [],
        photographer = [],
        date = '',
        bibliography = '',
        notes = '',
        keywords = [],
        copyright = '',
    } = {}) {
        this.name = name;
        this.language = language;
        this.script = script;
        this.provenance = provenance;
        this.location = location;
        this.photographer = photographer;
        this.date = date;
        this.bibliography = bibliography;
        this.notes = notes;
        this.keywords = keywords;
        this.copyright = copyright;
    }
}

export { Metadata }