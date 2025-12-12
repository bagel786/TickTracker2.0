export interface PricePoint {
    date: string;
    price: number;
}

export interface Event {
    id: string;
    name: string;
    venue: string;
    city: string;
    date: string;
    price_low: number | null;
    price_high: number | null;
    url: string;
    source: string;
    timezone: string | null;
}

export interface EventDetail extends Event {
    price_history: PricePoint[];
}

export interface Prediction {
    prediction: 'buy' | 'wait' | 'monitor';
    confidence: number;
    next_7_days_projection: number[];
}

export interface SearchEventsParams {
    query?: string;
    location?: string;
    start_date?: string;
    end_date?: string;
}
