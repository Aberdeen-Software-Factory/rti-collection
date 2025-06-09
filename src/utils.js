import artifactList from './components/data.js'

function getArtifact(id) {
    return artifactList.find(item => item.id === id);
}

function getArtifacts() {
    return artifactList;
}

export { getArtifacts, getArtifact }