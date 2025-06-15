const scriptLoadMap = new Map();

function loadScript(src) {
  if (scriptLoadMap.has(src)) {
    return scriptLoadMap.get(src); // Return the existing Promise
  }

  const promise = new Promise((resolve, reject) => {
    const existingScript = document.querySelector(`script[src="${src}"]`);

    if (existingScript) {
      if (existingScript.hasAttribute('data-loaded')) {
        resolve();
      } else {
        // Attach listeners in case it's still loading
        existingScript.addEventListener('load', resolve, { once: true });
        existingScript.addEventListener('error', reject, { once: true });
      }
      return;
    }

    const script = document.createElement('script');
    script.src = src;
    script.async = true;

    script.onload = () => {
      script.setAttribute('data-loaded', 'true');
      resolve();
    };
    script.onerror = reject;

    document.head.appendChild(script);
  });

  scriptLoadMap.set(src, promise);
  return promise;
}

function loadStyle(href) {
  if (!document.querySelector(`link[href="${href}"]`)) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = href
    document.head.appendChild(link)
  }
}

export { loadScript, loadStyle }