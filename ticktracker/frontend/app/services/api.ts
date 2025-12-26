// Redirecting to the correct API configuration
import { searchEvents, getEventDetails, getPrediction } from '../lib/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ticktracker-backend-production.up.railway.app';

export { API_BASE_URL };
export { searchEvents, getEventDetails, getPrediction };
