'use client';

import React, { useState, useMemo, useEffect } from 'react';
import {
    LineChart,
    Line,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    ReferenceLine,
    ReferenceArea,
    ComposedChart
} from 'recharts';
import { format } from 'date-fns';

interface EnhancedPriceChartProps {
    eventId: string;
    className?: string;
}

interface ChartLayer {
    id: string;
    name: string;
    enabled: boolean;
    color: string;
}

// Interfaces matching the API response
interface PricePoint {
    date: string;
    price: number;
    confidence?: number;
    data_source?: string;
    is_outlier?: boolean;
}

interface PredictionPoint {
    date: string;
    predicted_price: number;
    confidence_lower: number;
    confidence_upper: number;
}

interface Milestone {
    date: string;
    title: string;
    type: string;
}

interface SimilarEvent {
    event_name: string;
    price_data: PricePoint[];
}

interface BuyWindow {
    start_date: string;
    end_date: string;
    expected_price: number;
    reason: string;
}

interface ChartStatistics {
    current_price: number | null;
    price_trend: string;
    recommendation: string;
    volatility: number;
}

interface EnhancedChartData {
    historical_prices: PricePoint[];
    predictions: PredictionPoint[];
    milestones: Milestone[];
    similar_events: SimilarEvent[];
    buy_windows: BuyWindow[];
    statistics: ChartStatistics;
}

const ChartControls = ({ timeRange, onTimeRangeChange, layers, onLayerToggle, statistics }: any) => {
    return (
        <div className="flex flex-col gap-4 mb-4 bg-gray-50 p-4 rounded-lg border border-gray-200 text-gray-900">
            {/* Top Row: Stats & Recommendation */}
            <div className="flex flex-wrap justify-between items-center gap-4">
                <div className="flex gap-4 items-center">
                    <div className="px-3 py-1 bg-white rounded shadow-sm border text-sm">
                        <span className="text-gray-500 mr-2">Trend:</span>
                        <span className={`font-semibold ${statistics?.price_trend === 'increasing' ? 'text-red-500' : 'text-green-500'}`}>
                            {statistics?.price_trend?.toUpperCase() || '-'}
                        </span>
                    </div>
                    <div className="px-3 py-1 bg-white rounded shadow-sm border text-sm">
                        <span className="text-gray-500 mr-2">Action:</span>
                        <span className={`font-bold ${statistics?.recommendation === 'buy' ? 'text-green-600' : 'text-yellow-600'}`}>
                            {statistics?.recommendation?.toUpperCase() || '-'}
                        </span>
                    </div>
                </div>

                {/* Time Range Selector */}
                <div className="flex bg-white rounded-md border border-gray-300 overflow-hidden text-sm">
                    {['1w', '1m', '3m', 'all'].map((range) => (
                        <button
                            key={range}
                            onClick={() => onTimeRangeChange(range)}
                            className={`px-3 py-1.5 hover:bg-gray-50 ${timeRange === range ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600'}`}
                        >
                            {range.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>

            {/* Bottom Row: Layers */}
            <div className="flex flex-wrap gap-2 pt-2 border-t border-gray-200">
                {layers.map((layer: ChartLayer) => (
                    <button
                        key={layer.id}
                        onClick={() => onLayerToggle(layer.id)}
                        className={`flex items-center gap-2 px-2 py-1 rounded text-xs border transition-colors ${layer.enabled
                            ? 'bg-white border-blue-200 text-gray-800 shadow-sm'
                            : 'bg-gray-100 border-transparent text-gray-400'
                            }`}
                    >
                        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: layer.enabled ? layer.color : '#cbd5e1' }} />
                        {layer.name}
                    </button>
                ))}
            </div>
        </div>
    );
};

const CustomTooltip = ({ active, payload, label, data }: any) => {
    if (active && payload && payload.length) {
        // const pointData = payload[0].payload; 
        return (
            <div className="bg-white p-3 border border-gray-200 shadow-lg rounded text-sm z-50 opacity-95 text-gray-900">
                <p className="font-semibold text-gray-700 mb-1">{format(new Date(label), 'MMM d, yyyy')}</p>

                {payload.map((entry: any, index: number) => (
                    <div key={index} className="flex items-center gap-2 mb-1" style={{ color: entry.color }}>
                        <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: entry.color }}></span>
                        <span>{entry.name}:</span>
                        <span className="font-mono font-medium">${entry.value.toFixed(2)}</span>
                    </div>
                ))}

                {/* Show milestones if any on this date */}
                {data?.milestones?.filter((m: Milestone) => format(new Date(m.date), 'yyyy-MM-dd') === format(new Date(label), 'yyyy-MM-dd')).map((m: Milestone, idx: number) => (
                    <div key={idx} className="mt-2 pt-2 border-t border-gray-100 text-xs text-red-500">
                        <span className="font-bold">📢 {m.title}</span>: {m.type}
                    </div>
                ))}
            </div>
        );
    }
    return null;
};

export default function EnhancedPriceChart({ eventId, className }: EnhancedPriceChartProps) {
    // State management
    const [timeRange, setTimeRange] = useState<'1w' | '1m' | '3m' | 'all'>('all');
    const [layers, setLayers] = useState<ChartLayer[]>([
        { id: 'historical', name: 'Historical Prices', enabled: true, color: '#3b82f6' },
        { id: 'predictions', name: 'Predictions', enabled: true, color: '#8b5cf6' },
        { id: 'confidence', name: 'Confidence Interval', enabled: false, color: '#c7d2fe' },
        { id: 'similar', name: 'Similar Events', enabled: false, color: '#94a3b8' },
        { id: 'buyWindows', name: 'Buy Windows', enabled: true, color: '#10b981' }
    ]);

    const [data, setData] = useState<EnhancedChartData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            try {
                const res = await fetch(`${apiUrl}/api/events/${eventId}/chart-data?time_range=${timeRange}`);
                if (!res.ok) throw new Error('Failed to fetch chart data');
                const jsonData = await res.json();
                setData(jsonData);
            } catch (err: any) {
                console.error(err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [eventId, timeRange]);

    // Process data for chart
    const chartData = useMemo(() => {
        if (!data) return [];

        const pointsMap = new Map();

        // Historical
        data.historical_prices.forEach(h => {
            const d = new Date(h.date).toISOString().split('T')[0];
            if (!pointsMap.has(d)) pointsMap.set(d, { date: h.date });
            const p = pointsMap.get(d);
            p.historicalPrice = h.price;
        });

        // Predictions
        data.predictions.forEach(h => {
            const d = new Date(h.date).toISOString().split('T')[0];
            if (!pointsMap.has(d)) pointsMap.set(d, { date: h.date });
            const p = pointsMap.get(d);
            p.predictedPrice = h.predicted_price;
            p.confidenceUpper = h.confidence_upper;
            p.confidenceLower = h.confidence_lower;
        });

        const result = Array.from(pointsMap.values()).sort((a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime());
        return result;
    }, [data]);

    const toggleLayer = (layerId: string) => {
        setLayers(prev =>
            prev.map(layer =>
                layer.id === layerId ? { ...layer, enabled: !layer.enabled } : layer
            )
        );
    };

    if (loading) return <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg animate-pulse text-gray-500">Loading Chart Data...</div>;
    if (error) return <div className="h-64 flex items-center justify-center text-red-500 bg-red-50 rounded-lg">Error: {error}</div>;

    return (
        <div className={`w-full space-y-4 ${className}`}>
            {/* Chart Controls */}
            <ChartControls
                timeRange={timeRange}
                onTimeRangeChange={setTimeRange}
                layers={layers}
                onLayerToggle={toggleLayer}
                statistics={data?.statistics}
            />

            {/* Main Chart */}
            <div className="bg-white rounded-lg border border-gray-200 p-4">
                <ResponsiveContainer width="100%" height={400}>
                    <ComposedChart
                        data={chartData}
                        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                        <defs>
                            <linearGradient id="confidenceGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.05} />
                            </linearGradient>
                        </defs>

                        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />

                        <XAxis
                            dataKey="date"
                            tickFormatter={(date) => format(new Date(date), 'MMM d')}
                            stroke="#94a3b8"
                            fontSize={12}
                            tickMargin={10}
                        />

                        <YAxis
                            tickFormatter={(value) => `$${value}`}
                            stroke="#94a3b8"
                            fontSize={12}
                        />

                        <Tooltip content={<CustomTooltip data={data} />} />
                        <Legend wrapperStyle={{ paddingTop: '20px' }} />

                        {/* Confidence Interval Area */}
                        {layers.find(l => l.id === 'confidence')?.enabled && (
                            <Area
                                type="monotone"
                                dataKey="confidenceUpper"
                                stroke="none"
                                fill="url(#confidenceGradient)"
                            />
                        )}

                        {/* Buy Windows */}
                        {layers.find(l => l.id === 'buyWindows')?.enabled &&
                            data?.buy_windows.map((window: BuyWindow, idx: number) => (
                                <ReferenceArea
                                    key={`window-${idx}`}
                                    x1={window.start_date}
                                    x2={window.end_date}
                                    fill="#10b981"
                                    fillOpacity={0.15}
                                    strokeOpacity={0}
                                    label={{ value: 'BUY', position: 'insideTop', fill: '#059669', fontSize: 10 }}
                                />
                            ))
                        }

                        {/* Milestones */}
                        {data?.milestones.map((milestone: Milestone, idx: number) => (
                            <ReferenceLine
                                key={`milestone-${idx}`}
                                x={milestone.date}
                                stroke="#ef4444"
                                strokeDasharray="3 3"
                                label={{
                                    value: '🚩',
                                    position: 'top',
                                    fontSize: 14
                                }}
                            />
                        ))}

                        {/* Historical Prices Line */}
                        {layers.find(l => l.id === 'historical')?.enabled && (
                            <Line
                                type="monotone"
                                dataKey="historicalPrice"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                dot={{ fill: '#3b82f6', r: 3 }}
                                activeDot={{ r: 6 }}
                                name="History"
                                connectNulls
                            />
                        )}

                        {/* Predicted Prices Line */}
                        {layers.find(l => l.id === 'predictions')?.enabled && (
                            <Line
                                type="monotone"
                                dataKey="predictedPrice"
                                stroke="#8b5cf6"
                                strokeWidth={2}
                                strokeDasharray="5 5"
                                dot={{ fill: '#8b5cf6', r: 3 }}
                                name="Forecast"
                                connectNulls
                            />
                        )}

                    </ComposedChart>
                </ResponsiveContainer>
            </div>

            <div className="text-xs text-gray-400 text-center">
                * Predictions are ML-generated estimates. Not financial advice.
            </div>
        </div>
    );
}
