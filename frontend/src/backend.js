import Artifact from "@/models/Artifact";
import ArtifactPreview from "@/models/ArtifactPreview";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
console.log("Base url:", API_BASE_URL);

async function fetchArtifacts() {
    try {
        const res = await fetch(new URL('/artifacts', API_BASE_URL));
        
        if (!res.ok) throw new Error('Failed to fetch artifacts');
        
        const data = await res.json();
        console.log(data)
        return data.artifacts.map(obj => new ArtifactPreview(obj));
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function fetchArtifact(id) {
    try {
        const res = await fetch(new URL(`/artifacts/${id}`, API_BASE_URL));
        
        if (!res.ok) throw new Error(`Failed to fetch artifact with id ${id}`);
        
        const data = await res.json();
        return new Artifact(data.artifact);
    } catch (error) {
        console.error(error);
        throw error;
    }
}

function assembleFormData({ metadata, images, webrtis, ptms }) {
    const formData = new FormData();
    console.log(webrtis);
    if (metadata) {
        formData.append('metadata', JSON.stringify(metadata));
    }
    
    if (images) {
        for (const file of images) {
            formData.append('images', file)
        }
    }
    if (webrtis) {
        for (const file of webrtis) {
            formData.append('webrtis', file)
        }
    }
    if (ptms) {
        for (const file of ptms) {
            formData.append('ptms', file)
        }
    }
    // if (images) {
    //     for (const file of images) {
    //         formData.append('images', file);
    //     }
    // }
    
    // if (RTIs) {
    //     for (const [i, RTI] of RTIs.entries()) {
    //         const RTIKey = `RTI_${i + 1}`;
    //         formData.append('RTIKeys', RTIKey);
    //         for (const file of RTI) {
    //             formData.append(RTIKey, file);
    //         }
    //     }
    // }
    
    console.log('FormData contents:', [...formData.entries()]);
    return formData;
}

async function createArtifact({ metadata, images, webrtis, ptms }) {
    const username = '';
    const password = prompt("Enter your password:");
    const credentials = btoa(`${username}:${password}`);
    
    const formData = assembleFormData({ metadata, images, webrtis, ptms });
    
    const res = await fetch(new URL('/artifacts', API_BASE_URL), {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${credentials}`
        },
        body: formData,
    });
    
    if (!res.ok) {
        throw Error(`Upload failed with status: ${res.status}`);
    }
    
    const data = await res.json();
    return data;
    
}

async function updateArtifact(id, { metadata, images, webrtis, ptms }) {
    const username = '';
    const password = prompt("Enter your password:");
    const credentials = btoa(`${username}:${password}`);
    
    const formData = assembleFormData({ metadata, images, webrtis, ptms });
    
    const res = await fetch(new URL(`/artifacts/${id}`, API_BASE_URL), {
        method: 'PUT',
        headers: {
            'Authorization': `Basic ${credentials}`
        },
        body: formData
    });
    
    if (!res.ok) {
        throw Error('Upload failed with status:', res.status);
    }
    
    const data = await res.json();
    return data;
}

async function deleteArtifact(id) {
    const username = '';
    const password = prompt("Enter your password:");
    const credentials = btoa(`${username}:${password}`);
    
    const res = await fetch(new URL(`/artifacts/${id}`, API_BASE_URL), {
        method: 'DELETE',
        headers: {
            'Authorization': `Basic ${credentials}`
        },
    });
    
    if (!res.ok) {
        throw Error('Upload failed with status:', res.status);
    }
    
    const data = await res.json();
    return data;
}

export { fetchArtifacts, fetchArtifact, createArtifact, updateArtifact, deleteArtifact, assembleFormData }