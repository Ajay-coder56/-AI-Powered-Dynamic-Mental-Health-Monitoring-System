import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config';

const publicRoutes = [
  '/api/v1/auth/login',
  '/api/v1/users', // Victim flows don't have JWT auth yet
  '/health'
];

export const verifyToken = (req: Request, res: Response, next: NextFunction) => {
  // Let FastAPI handle token validation
  next();
};
