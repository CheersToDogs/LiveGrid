// Cloudflare Pages Function: /api/xhl/models
// Proxies xhamsterlive.com API to avoid CORS restriction

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const params = url.searchParams;

  const upstream = new URL('https://xhamsterlive.com/api/front/models');
  // Forward all query params
  for (const [k, v] of params.entries()) {
    upstream.searchParams.set(k, v);
  }

  const resp = await fetch(upstream.toString(), {
    headers: { 'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0' }
  });

  if (!resp.ok) {
    return new Response(JSON.stringify({ error: 'upstream ' + resp.status }), {
      status: resp.status,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  const data = await resp.text();
  return new Response(data, {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=15'
    }
  });
}
