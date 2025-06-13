import { Artifact, ArtifactPreview } from "./model/artifact";

const BACKEND = new URL('http://localhost:8000')

async function fetchArtifacts() {
    try {
        const res = await fetch(new URL('/artifacts', BACKEND));
        
        if (!res.ok) throw new Error('Failed to fetch artifacts');
        
        const data = await res.json();
        return data.artifacts.map(obj => new ArtifactPreview(obj));
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function fetchArtifact(id) {
    try {
        const res = await fetch(new URL(`/artifacts/${id}`, BACKEND));
        
        if (!res.ok) throw new Error(`Failed to fetch artifact with id ${id}`);
        
        const data = await res.json();
        return new Artifact(data.artifact);
    } catch (error) {
        console.error(error);
        throw error;
    }
}

function assembleFormData({ metadata, images, RTIs }) {
    const formData = new FormData();
    console.log(metadata);
    if (metadata) {
        formData.append('metadata', JSON.stringify(metadata));
    }
    
    if (images) {
        for (const file of images) {
            formData.append('images', file);
        }
    }

    if (RTIs) {
        for (const [i, RTI] of RTIs.entries()) {
            const RTIKey = `RTI_${i + 1}`;
            formData.append('RTIKeys', RTIKey);
            for (const file of RTI) {
                formData.append(RTIKey, file);
            }
        }
    }

    console.log('FormData contents:', [...formData.entries()]);
    return formData;
}

async function createArtifact({ metadata, images, RTIs }) {
    const formData = assembleFormData({ metadata, images, RTIs });

    try {
        const res = await fetch(new URL('/artifacts', BACKEND), {
            method: 'POST',
            body: formData
        });
        
        if (!res.ok) {
            throw Error('Upload failed with status:', res.status);
        }

        const data = await res.json();
        return data;
    } catch (error) {
        console.error('Upload failed:', error);
        throw error;
    }
}

async function updateArtifact(id, { metadata, images, RTIs }) {
    const formData = assembleFormData({ metadata, images, RTIs });

    try {
        const res = await fetch(new URL(`/artifacts/${id}`, BACKEND), {
            method: 'PUT',
            body: formData
        });
        
        if (!res.ok) {
            throw Error('Upload failed with status:', res.status);
        }

        const data = await res.json();
        return data;
    } catch (error) {
        console.error('Upload failed:', error);
        throw error;
    }
}

export { fetchArtifacts, fetchArtifact, createArtifact, updateArtifact }