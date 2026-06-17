const CACHE_NAME = 'soundify-cache-v4';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/style.css',
    '/script.js',
    '/manifest.json',
    '/Gambar3.jpg',
    '/Gambar4.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(keys.map((key) => {
                if (key !== CACHE_NAME) return caches.delete(key);
            }));
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    
    // Abaikan API Youtube agar tidak bentrok
    if (event.request.url.includes('youtube.com') || event.request.url.includes('ytimg.com')) return;

    // Untuk API backend kita, kembalikan kosong jika offline
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request).catch(() => new Response(JSON.stringify({status: 'error', data: []}), {headers: {'Content-Type': 'application/json'}}))
        );
        return;
    }

    // Untuk web dan aset lainnya, Network-First lalu Fallback ke Cache
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});