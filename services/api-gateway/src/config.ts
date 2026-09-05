import dotenv from 'dotenv';
dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3001', 10),
  fastApiUrl: process.env.FASTAPI_URL || 'http://localhost:8001',
  jwtSecret: process.env.JWT_SECRET || 'supersecretjwtkey',
  corsOrigin: process.env.CORS_ORIGIN || 'http://localhost:8443',
};
