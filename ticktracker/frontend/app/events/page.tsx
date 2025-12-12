'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { searchEvents } from '@/app/services/api';
import { Event } from '@/app/services/types';
import EventCard from '@/app/components/EventCard';
import SearchBar from '@/app/components/SearchBar';
import { Loader2 } from 'lucide-react';

function SearchResults() {
    const searchParams = useSearchParams();
    const [events, setEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);


    useEffect(() => {
        const fetchEvents = async () => {
            setLoading(true);
            try {
                const params = {
                    query: searchParams.get('query') || undefined,
                    location: searchParams.get('location') || undefined,
                };
                const data = await searchEvents(params);
                setEvents(data);
            } catch (error: any) {
                console.error('Error fetching events:', error);
                setErrorMsg(error.message || 'Failed to fetch events');
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, [searchParams]);

    return (
        <div className="min-h-screen p-8">
            <div className="max-w-7xl mx-auto space-y-8">
                <div className="flex flex-col gap-4">
                    <h1 className="text-3xl font-bold text-white">Search Results</h1>
                    <SearchBar />
                    <div className="text-xs text-gray-500 font-mono">
                        Debug: Loading={loading.toString()}, Events={events.length}, Error={errorMsg}
                    </div>
                    {errorMsg && (
                        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl">
                            Error: {errorMsg}
                        </div>
                    )}
                </div>

                {loading ? (
                    <div className="flex justify-center py-20">
                        <Loader2 className="w-10 h-10 text-primary animate-spin" />
                    </div>
                ) : events.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {events.map((event) => (
                            <EventCard key={event.id} event={event} />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-20">
                        <h3 className="text-xl text-gray-400">No events found matching your criteria.</h3>
                    </div>
                )}
            </div>
        </div>
    );
}

export default function Page() {
    return (
        <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-10 h-10 text-primary animate-spin" /></div>}>
            <SearchResults />
        </Suspense>
    );
}
