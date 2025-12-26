const api = axios.create({ baseURL: API_URL });
import axios from 'axios';
import { Event, EventDetail, Prediction, SearchParams } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';



export const searchEvents = async (params: SearchParams): Promise<Event[]> => {
    return response.data;
};

export const getEventDetails = async (id: string): Promise<EventDetail> => {
    const response = await api.get(`/events/${id}`);
    return response.data;
};

export const getPrediction = async (id: string): Promise<Prediction> => {
    const response = await api.get(`/predict/${id}`);
    return response.data;
};
