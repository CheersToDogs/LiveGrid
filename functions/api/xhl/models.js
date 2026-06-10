// Cloudflare Pages Function: /api/xhl/models
// Routes via auth.mycamgirlz.com (AWS) to avoid CF Worker egress block on xhamsterlive

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const params = url.searchParams;

  const upstream = new URL('https://auth.mycamgirlz.com/xhl/models');
  for (const [k, v] of params.entries()) {
    upstream.searchParams.set(k, v);
  }

  try {
    const resp = await fetch(upstream.toString(), {
      headers: { 'Accept': 'application/json' }
    });
    const data = await resp.text();
    return new Response(data, {
      status: resp.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=15',
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }
}
