'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PriceHistory } from '../lib/types';

interface PriceChartProps {
    data: PriceHistory[];
    timezone?: string;
}

export default function PriceChart({ data, timezone }: PriceChartProps) {
    if (!data || data.length === 0) {
        return (
            <div className="h-[300px] flex items-center justify-center bg-white/5 rounded-xl border border-white/10">
                <p className="text-gray-400 text-center px-4">
                    No price data is available for this event because we don’t have enough historical pricing entries yet.
                </p>
            </div>
        );
    }

    const formattedData = data.map(item => ({
        ...item,
        date: new Date(item.timestamp).toLocaleDateString('en-US', {
            timeZone: timezone,
            month: 'numeric',
            day: 'numeric',
        }),
    }));

    return (
        <div className="h-[300px] w-full bg-white/5 p-4 rounded-xl border border-white/10">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={formattedData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                        dataKey="date"
                        stroke="#666"
                        tick={{ fill: '#666' }}
                    />
                    <YAxis
                        stroke="#666"
                        tick={{ fill: '#666' }}
                        tickFormatter={(value) => `$${value}`}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(value: number) => [`$${value}`, 'Price']}
                    />
                    <Line
                        type="monotone"
                        dataKey="price"
                        stroke="#6366f1"
                        strokeWidth={2}
                        dot={{ fill: '#6366f1' }}
                        activeDot={{ r: 8 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
