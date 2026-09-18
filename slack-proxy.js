// 로컬 프록시 서버 (Slack + Anthropic API)
// 실행: node slack-proxy.js
const http = require('http');
const https = require('https');

const PORT = 3002;

function httpsPost(hostname, path, headers, body) {
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname, path, method: 'POST', headers }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function httpsGet(hostname, path, headers) {
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname, path, method: 'GET', headers }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
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
        // Anthropic API 프록시
        const { apiKey, messages, model, max_tokens } = payload;
        const reqBody = JSON.stringify({ model, max_tokens, messages });
        const result = await httpsPost('api.anthropic.com', '/v1/messages', {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
        }, reqBody);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(result);

      } else {
        // Slack API 프록시
        const { token, endpoint, params } = payload;
        const query = new URLSearchParams(params || {}).toString();
        const path = `/api/${endpoint}${query ? '?' + query : ''}`;
        const result = await httpsGet('slack.com', path, {
          'Authorization': `Bearer ${token}`
        });
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(result);
      }

    } catch (e) {
      res.writeHead(500);
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  });
}).listen(PORT, () => console.log(`프록시 서버 실행 중: http://localhost:${PORT}`));
