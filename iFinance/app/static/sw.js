const staticCacheName = 'site-static';
const dynamicCacheName = 'site-dynamic';
const precachedResources = [
  '/ifinance/',
  '/ifinance/sw.js',
  '/ifinance/static/css/bootstrap.css',
  '/ifinance/static/js/app.js',
  '/ifinance/static/manifest.json',
  '/ifinance/static/css/style.css',
  'https://cdn.jsdelivr.net/npm/chart.js',
  '/ifinance/static/icons/icon-64x64.png',
  '/ifinance/static/icons/user.png',
  '/ifinance/static/icons/dashboard.png',
  '/ifinance/static/icons/project.png',
  '/ifinance/static/icons/icon-256x256.png',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js'
];
async function precache() {
  const cache = await caches.open(staticCacheName);
  return cache.addAll(precachedResources);
}


self.addEventListener('install', evt => {
  console.log('service worker installed');
  // evt.waitUntil(
  //   precache()
  // );
});

// //   // activate event
self.addEventListener('activate', evt => {
  console.log('service worker activated');
});

function isCacheable(request) {
  const url = new URL(request.url);
  return !url.pathname.endsWith(".json");
}

async function cacheFirstWithRefresh(request) {
  try {
    const fetchResponsePromise = fetch(request)
      .then(async (networkResponse) => {
        if (networkResponse.ok) {
          const cache = await caches.open(dynamicCacheName);
          cache.put(request, networkResponse.clone());
        }
        return networkResponse;
      });
  } catch (error) {
    console.log(error);
  }

  return (await caches.match(request)) || (await fetchResponsePromise);
}

self.addEventListener("fetch", (event) => {
  console.log('service worker installed');
  // if (isCacheable(event.request)) {
  //   event.respondWith(cacheFirstWithRefresh(event.request));
  // }
});

//   self.addEventListener('fetch', function (event) {
//     event.respondWith(
//         fetch(event.request).catch(function() {
//             return caches.match(event.request)
//         })
//     )
// })