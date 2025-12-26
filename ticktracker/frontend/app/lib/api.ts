import axios from 'axios';
import { Event, EventDetail, Prediction, SearchParams } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ticktracker-backend-production.up.railway.app';

const api = axios.create({ 
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const searchEvents = async (params: SearchParams): Promise<Event[]> => {
    try {
        const response = await api.get('/events/search', { params });
        return response.data;
    } catch (error) {
        console.error('API Error searchEvents:', error);
        throw error;
    }
};

export const getEventDetails = async (id: string): Promise<EventDetail> => {
    try {
        const response = await api.get(`/events/${id}`);
        return response.data;
    } catch (error) {
        console.error('API Error getEventDetails:', error);
        throw error;
    }
};

export const getPrediction = async (id: string): Promise<Prediction> => {
    try {
        const response = await api.get(`/predict/${id}`);
        return response.data;
    } catch (error) {
        console.error('API Error getPrediction:', error);
        throw error;
    }
};
