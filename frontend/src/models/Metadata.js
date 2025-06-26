import CCLicense from "@/models/CCLicense"

/**
 * Represents metadata for an artifact.
 */
export default class Metadata {
    /** @type {string} */
    name
    /** @type {string[]} */
    languages
    /** @type {string[]} */
    scripts
    /** @type {string[]} */
    provenances
    /** @type {string[]} */
    locations
    /** @type {string[]} */
    photographers
    /** @type {string} */
    date
    /** @type {string} */
    bibliography
    /** @type {string} */
    notes
    /** @type {string[]} */
    keywords
    /** @type {CCLicense} */
    copyright

    constructor(data = {}) {
        this.name = String(data.name || '')
        this.languages = (data.language || []).map(String)
        this.scripts = (data.script || []).map(String)
        this.provenances = (data.provenance || []).map(String)
        this.locations = (data.location || []).map(String)
        this.photographers = (data.photographer || []).map(String)
        this.date = String(data.date || '')
        this.bibliography = String(data.bibliography || '')
        this.notes = String(data.notes || '')
        this.keywords = (data.keywords || []).map(String)
        this.copyright = data.copyright || CCLicense.BY
    }
}
