// utils/patchFetchForFiles.js

let originalFetch = null;

export function patchFetchForFiles(fileMap) {
  console.log("patching", fileMap);
  if (!fileMap || typeof fileMap !== 'object') return;

  if (!originalFetch) {
    originalFetch = window.fetch;
  }

  window.fetch = async (input, init) => {
    const url = typeof input === 'string' ? input : input.url ?? input.href;
    const filename = url.split('/').pop();
    console.log("Intercepted fetch for:", filename, input);

    if (fileMap[filename]) {
      const blobUrl = fileMap[filename];
      console.log(`[fetch patch] Redirecting to blob URL for: ${filename} → ${blobUrl}`);
      return originalFetch(blobUrl, init);  // ✅ Correct: delegate to real fetch with blob URL
    }
    console.log(`[fetch patch] executing original fetch: ${filename} → ${input}`);
    return originalFetch(input, init);  // Default fallback
  };
}

export function restoreOriginalFetch() {
  if (originalFetch) {
    window.fetch = originalFetch;
    originalFetch = null;
    console.log('[fetch patch] Original fetch restored');
  }
}
