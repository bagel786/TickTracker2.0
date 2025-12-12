import { EventDetail, Prediction, Event, SearchEventsParams } from './types';

const API_BASE_URL = 'http://localhost:8000';

export async function searchEvents(params: SearchEventsParams): Promise<Event[]> {
    const queryParams = new URLSearchParams();
    if (params.query) queryParams.append('query', params.query);
    if (params.location) queryParams.append('location', params.location);
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);

    const res = await fetch(`${API_BASE_URL}/events/search?${queryParams.toString()}`, { cache: 'no-store' });
    if (!res.ok) {
        throw new Error('Failed to fetch events');
    }
    return res.json();
}

export async function getEventDetails(eventId: string): Promise<EventDetail> {
    const res = await fetch(`${API_BASE_URL}/events/${eventId}`, { cache: 'no-store' });
    if (!res.ok) {
        throw new Error('Failed to fetch event details');
    }
    return res.json();
}

export async function getPrediction(eventId: string): Promise<Prediction> {
    const res = await fetch(`${API_BASE_URL}/predict/${eventId}`, { cache: 'no-store' });
    if (!res.ok) {
        throw new Error('Failed to fetch prediction');
    }
    return res.json();
}
