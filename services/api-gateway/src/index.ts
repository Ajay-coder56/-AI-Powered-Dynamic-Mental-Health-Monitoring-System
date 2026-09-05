import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { config } from './config';
import { apiRateLimiter } from './middleware/rateLimiter';
import { verifyToken } from './middleware/auth';
import { fastApiProxy } from './proxy';
import './types'; // Import type definitions

const app = express();
const PORT = process.env.PORT || 3001;
const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8001';

// Security headers
app.use(helmet());

// Setup CORS (allow frontend)
const corsOptions = {origin: config.corsOrigin,
  credentials: true
};
app.use(cors(corsOptions));

// Request logging
app.use(morgan('combined'));

// Rate limiting globally
app.use(apiRateLimiter);

// Gateway Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({ status: 'ok', service: 'gateway', timestamp: new Date().toISOString() });
});

// Auth middleware for API routes
app.use('/api', verifyToken);

// Proxy authenticated /api/* requests to FastAPI backend
app.use('/api', fastApiProxy);

// Start the server
app.listen(config.port, () => {
  console.log(`API Gateway listening on http://localhost:${config.port}`);
  console.log(`Proxying requests to ${config.fastApiUrl}`);
  console.log(`Allowing CORS from ${config.corsOrigin}`);
});
