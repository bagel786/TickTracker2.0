'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, MapPin } from 'lucide-react';

export default function SearchBar() {
    const router = useRouter();
    const [query, setQuery] = useState('');
    const [location, setLocation] = useState('');

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        const params = new URLSearchParams();
        if (query) params.set('query', query);
        if (location) params.set('location', location);
        router.push(`/events?${params.toString()}`);
    };

    return (
        <form onSubmit={handleSearch} className="w-full max-w-3xl mx-auto">
            <div className="flex flex-col md:flex-row gap-4 p-2 bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl shadow-2xl">
                <div className="flex-1 flex items-center px-4 h-14 bg-white/5 rounded-xl border border-transparent focus-within:border-primary/50 transition-all">
                    <Search className="w-5 h-5 text-gray-400 mr-3" />
                    <input
                        type="text"
                        placeholder="Search artists, events, or venues..."
                        className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-500"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>
                <div className="flex-1 flex items-center px-4 h-14 bg-white/5 rounded-xl border border-transparent focus-within:border-primary/50 transition-all">
                    <MapPin className="w-5 h-5 text-gray-400 mr-3" />
                    <input
                        type="text"
                        placeholder="City or location..."
                        className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-500"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                    />
                </div>
                <button
                    type="submit"
                    className="h-14 px-8 bg-primary hover:bg-primary/90 text-white font-bold rounded-xl transition-all shadow-lg shadow-primary/25"
                >
                    Search
                </button>
            </div>
            <div className="mt-4 text-center">
                <a href="/transparency" className="text-xs text-gray-500 hover:text-white underline decoration-dotted transition-colors">
                    🔍 How our Model Works & Transparency
                </a>
            </div>
        </form>
    );
}
