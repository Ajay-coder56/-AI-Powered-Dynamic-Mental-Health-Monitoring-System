import { createProxyMiddleware } from 'http-proxy-middleware';
import { config } from './config';

export const fastApiProxy = createProxyMiddleware({
  target: config.fastApiUrl,
  changeOrigin: true,
  // pathRewrite: {
  //   '^/api': '/api', // keep or modify path as required by FastAPI
  // },
  onProxyReq: (proxyReq, req, res) => {
    // Optionally pass user details downstream
    // if (req.user) {
    //   proxyReq.setHeader('X-User', JSON.stringify(req.user));
    // }
  },
  onError: (err, req, res) => {
    console.error('Proxy Error:', err);
    // @ts-ignore
    res.status(502).json({ error: 'Bad Gateway: FastAPI backend is unreachable' });
  }
});
