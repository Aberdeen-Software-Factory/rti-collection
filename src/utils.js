import artifactList from './components/data.js'

function getArtifact(id) {
    return artifactList.find(item => item.id === id);
}

function getArtifacts() {
    return artifactList;
}

// async function fetchFiles(urls) {
//   const responses = await Promise.all(urls.map(url => fetch(url)))

//   // Check for any failed responses
//   responses.forEach((res, i) => {
//     if (!res.ok) {
//       console.error(`Failed to fetch ${urls[i]}: ${res.statusText}`)
//     }
//   })

//   // Convert each response to blob (or text/json/etc.)
//   const files = await Promise.all(responses.map(res => res.blob()))
//   return files
// }

async function fetchFiles(urls) {
  const responses = await Promise.all(urls.map(url => fetch(url)))

  // Warn on failed fetches
  responses.forEach((res, i) => {
    if (!res.ok) {
      console.error(`Failed to fetch ${urls[i]}: ${res.statusText}`)
    }
  })

  // Convert responses to File objects
  const files = await Promise.all(
    responses.map(async (res, i) => {
      const blob = await res.blob()

      // Try to extract a filename from the URL
      const url = urls[i]
      const name = url.split('/').pop() || `file${i}`

      return new File([blob], name, { type: blob.type })
    })
  )

  return files
}

export { getArtifacts, getArtifact, fetchFiles }