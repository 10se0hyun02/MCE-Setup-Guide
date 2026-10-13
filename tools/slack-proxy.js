// 로컬 프록시 서버 (Slack + Anthropic API)
// 실행: node slack-proxy.js
const http = require('http');
const https = require('https');

const PORT = 3099;

function httpsRequest(method, hostname, path, headers, body, timeoutMs = 30000) {
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname, path, method, headers }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 300 && res.statusCode < 400) {
          resolve(JSON.stringify({ ok: false, error: `redirect_${res.statusCode}`, location: res.headers.location }));
        } else {
          resolve(data);
        }
      });
    });
    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`요청 시간 초과 (${timeoutMs / 1000}초)`));
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.method !== 'POST') { res.writeHead(405); res.end(); return; }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    try {
      const payload = JSON.parse(body);

      if (payload.service === 'anthropic') {
        const { messages, model, max_tokens } = payload;
        const apiKey = (payload.apiKey || '').replace(/[^\x20-\x7E]/g, '').trim();
        console.log(`[Anthropic] model=${model} key=***${apiKey.slice(-4)}`);
        const reqBody = JSON.stringify({ model, max_tokens, messages });
        const result = await httpsRequest('POST', 'api.anthropic.com', '/v1/messages', {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
          'content-length': String(Buffer.byteLength(reqBody)),
        }, reqBody);
        console.log(`[Anthropic] 응답 길이: ${result.length}`);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(result);

      } else {
        const { token, endpoint, params } = payload;
        const query = new URLSearchParams(params || {}).toString();
        const path = `/api/${endpoint}${query ? '?' + query : ''}`;
        console.log(`[Slack] ${endpoint} ${query}`);
        const result = await httpsRequest('GET', 'slack.com', path, {
          'Authorization': `Bearer ${token}`,
        });
        try { JSON.parse(result); } catch(_) {
          console.error(`[Slack] non-JSON response:`, result.slice(0, 200));
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: false, error: 'non_json_response', raw: result.slice(0, 500) }));
          return;
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(result);
      }

    } catch (e) {
      console.error('[proxy error]', e.message);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  });
}).listen(PORT, () => console.log(`프록시 서버 실행 중: http://localhost:${PORT}`));
