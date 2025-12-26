'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PriceHistory } from '../lib/types';

interface PriceChartProps {
    data: PriceHistory[];
    timezone?: string;
}

export default function PriceChart({ data, timezone, eventDate }: { data: PriceHistory[], timezone?: string, eventDate?: string }) {
    const isSynthetic = !data || data.length === 0;

    // Generate synthetic data if no real data exists
    const chartData = isSynthetic ? generateHeuristicCurve(eventDate) : data.map(item => ({
        ...item,
        date: new Date(item.timestamp).toLocaleDateString('en-US', {
            timeZone: timezone,
            month: 'short',
            day: 'numeric',
        }),
    }));

    // Helper to generate a U-shaped heuristic curve
    function generateHeuristicCurve(eventDateString?: string) {
        if (!eventDateString) return [];
        const eventDt = new Date(eventDateString);
        const today = new Date();
        const daysUntil = Math.ceil((eventDt.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

        // Don't show curve if event is in the past
        if (daysUntil < 0) return [];

        const curvePoints = [];
        // Generate 7 points leading up to the event
        for (let i = 6; i >= 0; i--) {
            const d = new Date();
            d.setDate(today.getDate() + (6 - i) * (daysUntil / 7));

            // Simple heuristic shape: 
            // - Far out: High (100)
            // - Middle (sweet spot): Low (80)
            // - Close: High (120 - panic buying)
            // We'll normalize this curve to a 0-100 scale for "Demand Intensity"

            // Normalized time t where 0=now, 1=event
            const t = (6 - i) / 6;

            // U-shape formula: f(t) = 4(t-0.5)^2 + 0.5 (Rough parabola)
            let heuristicValue = 100 * (4 * Math.pow(t - 0.5, 2) + 0.2);

            curvePoints.push({
                date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                price: Math.round(heuristicValue),
                isProjection: true
            });
        }
        return curvePoints;
    }

    if (chartData.length === 0) {
        return (
            <div className="h-[300px] flex items-center justify-center bg-white/5 rounded-xl border border-white/10">
                <p className="text-gray-400 text-center px-4">
                    No price data or estimates available for this date.
                </p>
            </div>
        );
    }

    return (
        <div className="h-[300px] w-full bg-white/5 p-4 rounded-xl border border-white/10 relative">
            {isSynthetic && (
                <div className="absolute top-4 right-4 z-10 bg-yellow-500/10 border border-yellow-500/20 px-3 py-1 rounded-full">
                    <span className="text-xs text-yellow-500 font-medium">Estimated Demand Curve</span>
                </div>
            )}
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                        dataKey="date"
                        stroke="#666"
                        tick={{ fill: '#666' }}
                    />
                    <YAxis
                        stroke="#666"
                        tick={{ fill: '#666' }}
                        tickFormatter={(value) => isSynthetic ? '' : `$${value}`}
                        label={isSynthetic ? { value: 'Demand Intensity', angle: -90, position: 'insideLeft', fill: '#666' } : undefined}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(value: number) => [isSynthetic ? `${value} (Index)` : `$${value}`, isSynthetic ? 'Demand Level' : 'Price']}
                        labelFormatter={(label) => `Date: ${label}`}
                    />
                    <Line
                        type="monotone"
                        dataKey="price"
                        stroke={isSynthetic ? "#fbbf24" : "#6366f1"}
                        strokeDasharray={isSynthetic ? "5 5" : undefined}
                        strokeWidth={2}
                        dot={{ fill: isSynthetic ? "#fbbf24" : "#6366f1" }}
                        activeDot={{ r: 8 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
