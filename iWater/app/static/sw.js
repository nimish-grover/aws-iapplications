const staticCacheName = 'site-static-v1.0.0';
const dynamicCacheName = 'site-dynamic-v1.0.2';
const precachedResources = [
  '/style.css',
  '/favicon.ico',
  '/app.js',
  '/manifest.json',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  'https://bootswatch.com/5/pulse/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

// Precache
async function precache() {
  const cache = await caches.open(staticCacheName);
  return cache.addAll(precachedResources);
}

// install event
self.addEventListener('install', evt => {
    console.log('service worker has been installed');
    // evt.waitUntil(precache());
  });

  // activate event
self.addEventListener('activate', evt => {
  //console.log('service worker activated');
  // evt.waitUntil(
  //   caches.keys().then(keys => {
  //     //console.log(keys);
  //     return Promise.all(keys
  //       .filter(key => key !== staticCacheName && key !== dynamicCacheName)
  //       .map(key => caches.delete(key))
  //     );
  //   })
  // );
});

// async function networkFirst(request) {
//   try {
//     const networkResponse = await fetch(request);
//     if (networkResponse.ok) {
//       const cache = await caches.open("MyCache_1");
//       cache.put(request, networkResponse.clone());
//     }
//     return networkResponse;
//   } catch (error) {
//     const cachedResponse = await caches.match(request);
//     return cachedResponse || Response.error();
//   }
// }

// self.addEventListener("fetch", (event) => {
//   const url = new URL(event.request.url);
//   if (url.pathname.match(/^\/inbox/)) {
//     event.respondWith(networkFirst(event.request));
//   }
// });

// Cache First with refresh
function isCacheable(request) {
  const url = new URL(request.url);
  return !url.pathname.endsWith(".json");
}

async function cacheFirstWithRefresh(request) {
  const fetchResponsePromise = fetch(request).then(async (networkResponse) => {
    if (networkResponse.ok) {
      const cache = await caches.open(dynamicCacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  });

  return (await caches.match(request)) || (await fetchResponsePromise);
}

// Network first
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(dynamicCacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    return cachedResponse || Response.error();
  }
}

// fetch event
self.addEventListener('fetch', evt => {
  // if (isCacheable(evt.request)) {
  //   evt.respondWith(cacheFirstWithRefresh(evt.request));
  // }
  // const url = new URL(evt.request.url);
  // if (url.pathname.match(/^\/pwa/)) {
  //   evt.respondWith(networkFirst(evt.request));
  // }
  // if(evt.request.url.indexOf('about') > -1){
  //   console.log('TRUE');
  // } else {
  //   console.log('FALSE');
  // };
  //console.log('fetch event', evt);
  // evt.respondWith(
  //   caches.match(evt.request).then(cacheRes => {
  //     return cacheRes || fetch(evt.request).then(fetchRes => {
  //       return caches.open(dynamicCacheName).then(cache => {
  //         cache.put(evt.request.url, fetchRes.clone());
  //         // check cached items size
  //         limitCacheSize(dynamicCacheName, 15);
  //         return fetchRes;
  //       })
  //     });
  //   }).catch(() => {
  //     caches.match('/error');
  //     // if(evt.request.url.indexOf('.html') > -1){
  //     //   return caches.match('/pages/fallback.html');
  //     // } 
  //   })
  // );
});
  // self.addEventListener('fetch', evt => {
  //   //console.log('fetch event', evt);
  //   evt.respondWith(
  //     // caches.match(evt.request).then(cacheRes => {
  //     //   return cacheRes || fetch(evt.request);
  //     // })
  //     caches.match(evt.request).then(cacheRes => {
  //       return cacheRes || fetch(evt.request).then(async fetchRes => {
  //         const cache = await caches.open(dynamicCacheName);
  //         cache.put(evt.request.url, fetchRes.clone());
  //         // check cached items size
  //         limitCacheSize(dynamicCacheName, 15);
  //         return fetchRes;
  //       });
  //     }).catch(() => {
  //       caches.match('/error');
  //       // if(evt.request.url.indexOf('.html') > -1){
  //       //   return caches.match('/error');
  //       // } 
  //     })
  //   );
  // });