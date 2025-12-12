'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getEventDetails, getPrediction } from '@/app/lib/api';
import { EventDetail, Prediction } from '@/app/lib/types';
import PriceChart from '@/app/components/PriceChart';
import { Loader2, Calendar, MapPin, ExternalLink, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export default function EventPage() {
    const params = useParams();
    const [event, setEvent] = useState<EventDetail | null>(null);
    const [prediction, setPrediction] = useState<Prediction | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            if (!params.id) return;
            try {
                const [eventData, predictionData] = await Promise.all([
                    getEventDetails(params.id as string),
                    getPrediction(params.id as string)
                ]);
                setEvent(eventData);
                setPrediction(predictionData);
            } catch (error) {
                console.error('Error fetching event details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [params.id]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-10 h-10 text-primary animate-spin" />
            </div>
        );
    }

    if (!event) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <h1 className="text-2xl text-gray-400">Event not found</h1>
            </div>
        );
    }

    const getPredictionColor = (pred: string) => {
        switch (pred) {
            case 'buy': return 'text-green-400';
            case 'wait': return 'text-red-400';
            default: return 'text-yellow-400';
        }
    };

    const getPredictionIcon = (pred: string) => {
        switch (pred) {
            case 'buy': return <TrendingDown className="w-6 h-6" />;
            case 'wait': return <TrendingUp className="w-6 h-6" />;
            default: return <Minus className="w-6 h-6" />;
        }
    };

    return (
        <div className="min-h-screen p-8">
            <div className="max-w-7xl mx-auto grid lg:grid-cols-3 gap-8">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-8">
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-4">{event.name}</h1>
                        <div className="flex flex-wrap gap-6 text-gray-400">
                            <div className="flex items-center gap-2">
                                <Calendar className="w-5 h-5" />
                                <span>{new Date(event.date).toLocaleString('en-US', {
                                    weekday: 'short',
                                    month: 'short',
                                    day: 'numeric',
                                    hour: 'numeric',
                                    minute: 'numeric',
                                    timeZone: event.timezone || undefined,
                                    timeZoneName: 'short'
                                })}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <MapPin className="w-5 h-5" />
                                <span>{event.venue}, {event.city}</span>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-2xl font-bold text-white">Price History</h2>
                        <PriceChart data={event.price_history} timezone={event.timezone} />
                    </div>
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                    {/* Prediction Card */}
                    <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-lg">
                        <h3 className="text-lg font-medium text-gray-400 mb-4">AI Recommendation</h3>
                        {prediction && (
                            <div className="space-y-4">
                                <div className={`flex items-center gap-3 text-3xl font-bold ${getPredictionColor(prediction.prediction)}`}>
                                    {getPredictionIcon(prediction.prediction)}
                                    <span className="uppercase">{prediction.prediction} NOW</span>
                                </div>

                                <div className="space-y-2">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-400">Confidence Score</span>
                                        <span className="text-white font-bold">{(prediction.confidence * 100).toFixed(0)}%</span>
                                    </div>
                                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-primary transition-all duration-500"
                                            style={{ width: `${prediction.confidence * 100}%` }}
                                        />
                                    </div>
                                </div>

                                <p className="text-sm text-gray-400 pt-4 border-t border-white/10">
                                    Based on historical trends, we predict prices will {prediction.prediction === 'buy' ? 'rise' : 'fall'} in the next 7 days.
                                </p>
                            </div>
                        )}
                    </div>

                    {/* Price Info */}
                    <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                        <h3 className="text-lg font-medium text-gray-400 mb-4">Current Prices</h3>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <span className="text-gray-400">Lowest Price</span>
                                <span className="text-2xl font-bold text-white">
                                    {event.price_low ? `$${event.price_low}` : 'N/A'}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-gray-400">Highest Price</span>
                                <span className="text-2xl font-bold text-white">
                                    {event.price_high ? `$${event.price_high}` : 'N/A'}
                                </span>
                            </div>

                            {event.source && event.source.includes("(Est.)") && (
                                <div className="mt-2 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                                    <p className="text-yellow-500 text-xs font-medium">
                                        ⚠️ These are estimated prices based on historical data, not verified real-time listings.
                                    </p>
                                </div>
                            )}

                            <a
                                href={event.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block w-full py-3 bg-primary hover:bg-primary/90 text-white text-center font-bold rounded-xl transition-all flex items-center justify-center gap-2 mt-6"
                            >
                                Buy Tickets <ExternalLink className="w-4 h-4" />
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
