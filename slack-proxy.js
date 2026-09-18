// Slack API 프록시 서버 (Node.js 내장 모듈만 사용)
// 실행: node slack-proxy.js
const http = require('http');
const https = require('https');

const PORT = 3002;

http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.method !== 'POST') { res.writeHead(405); res.end(); return; }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    try {
      const { token, endpoint, params } = JSON.parse(body);
      const query = new URLSearchParams(params || {}).toString();
      const options = {
        hostname: 'slack.com',
        path: `/api/${endpoint}${query ? '?' + query : ''}`,
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      };
      const proxyReq = https.request(options, proxyRes => {
        let data = '';
        proxyRes.on('data', chunk => data += chunk);
        proxyRes.on('end', () => {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(data);
        });
      });
      proxyReq.on('error', err => {
        res.writeHead(500);
        res.end(JSON.stringify({ ok: false, error: err.message }));
      });
      proxyReq.end();
    } catch (e) {
      res.writeHead(400);
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  });
}).listen(PORT, () => console.log(`Slack proxy: http://localhost:${PORT}`));
