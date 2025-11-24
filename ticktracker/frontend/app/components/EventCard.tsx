import Link from 'next/link';
import { Event } from '@/app/lib/types';
import { Calendar, MapPin, Ticket, AlertCircle } from 'lucide-react';
import { useState } from 'react';
import ReportPriceModal from './ReportPriceModal';

interface EventCardProps {
    event: Event;
}

export default function EventCard({ event }: EventCardProps) {
    const [isReportModalOpen, setIsReportModalOpen] = useState(false);

    const date = new Date(event.date).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    });

    const isEstimated = event.source.toLowerCase().includes('heuristic') || event.source.toLowerCase().includes('est');

    return (
        <>
            <div className="block group relative">
                <Link href={`/events/${event.id}`}>
                    <div className="bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10">
                        <div className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-xl font-bold text-white group-hover:text-primary transition-colors line-clamp-2 pr-8">
                                    {event.name}
                                </h3>
                            </div>

                            <div className="space-y-2 text-gray-400 text-sm mb-6">
                                <div className="flex items-center gap-2">
                                    <Calendar className="w-4 h-4" />
                                    <span>{date}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <MapPin className="w-4 h-4" />
                                    <span>{event.venue}, {event.city}</span>
                                </div>
                            </div>

                            <div className="flex items-center justify-between pt-4 border-t border-white/10">
                                <div className="flex flex-col">
                                    <span className="text-xs text-gray-500">Price Range</span>
                                    <span className="text-lg font-bold text-white flex items-center gap-2">
                                        {event.price_low ? `$${event.price_low}` : 'N/A'} - {event.price_high ? `$${event.price_high}` : 'N/A'}
                                        {isEstimated && <span className="text-xs font-normal text-orange-400 bg-orange-400/10 px-1.5 py-0.5 rounded">(Est.)</span>}
                                    </span>
                                </div>
                                <div className="bg-white/10 p-2 rounded-lg group-hover:bg-primary group-hover:text-white transition-colors">
                                    <Ticket className="w-5 h-5" />
                                </div>
                            </div>
                        </div>
                    </div>
                </Link>

                {/* Report Price Button - Positioned absolutely or relative to card, but outside the Link to prevent navigation */}
                <button
                    onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        setIsReportModalOpen(true);
                    }}
                    className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity bg-red-500/10 hover:bg-red-500/20 text-red-400 p-1.5 rounded-lg text-xs flex items-center gap-1"
                    title="Report incorrect price"
                >
                    <AlertCircle className="w-3 h-3" />
                    <span>Report</span>
                </button>
            </div>

            <ReportPriceModal
                isOpen={isReportModalOpen}
                onClose={() => setIsReportModalOpen(false)}
                eventId={event.id}
                eventName={event.name}
            />
        </>
    );
}
