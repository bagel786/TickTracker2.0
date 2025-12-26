"use client";

import { useState } from 'react';
import { X } from 'lucide-react';

interface ReportPriceModalProps {
    isOpen: boolean;
    onClose: () => void;
    eventId: string;
    eventName: string;
}

export default function ReportPriceModal({ isOpen, onClose, eventId, eventName }: ReportPriceModalProps) {
    const [price, setPrice] = useState('');
    const [sourceUrl, setSourceUrl] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsSubmitting(true);

        try {
            const priceValue = parseFloat(price);
            if (isNaN(priceValue) || priceValue <= 0) {
                throw new Error("Please enter a valid positive price.");
            }

            const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://ticktracker-backend-production.up.railway.app';
            const response = await fetch(`${API_BASE}/events/${eventId}/report-price`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    price: priceValue,
                    source_url: sourceUrl || null
                }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || "Failed to submit report");
            }

            setSuccess(true);
            setTimeout(() => {
                onClose();
                setSuccess(false);
                setPrice('');
                setSourceUrl('');
            }, 2000);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
            <div className="bg-gray-900 border border-white/10 rounded-2xl w-full max-w-md p-6 shadow-xl">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-white">Report Price</h3>
                    <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {success ? (
                    <div className="text-center py-8">
                        <div className="w-12 h-12 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                        </div>
                        <h4 className="text-lg font-semibold text-white mb-2">Thank You!</h4>
                        <p className="text-gray-400">Your report has been submitted for review.</p>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-1">
                                Event
                            </label>
                            <div className="text-white font-medium">{eventName}</div>
                        </div>

                        <div>
                            <label htmlFor="price" className="block text-sm font-medium text-gray-400 mb-1">
                                Actual Price Found ($)
                            </label>
                            <input
                                type="number"
                                id="price"
                                step="0.01"
                                min="0"
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary transition-colors"
                                placeholder="e.g. 150.00"
                                required
                            />
                        </div>

                        <div>
                            <label htmlFor="url" className="block text-sm font-medium text-gray-400 mb-1">
                                Source URL (Optional)
                            </label>
                            <input
                                type="url"
                                id="url"
                                value={sourceUrl}
                                onChange={(e) => setSourceUrl(e.target.value)}
                                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary transition-colors"
                                placeholder="https://..."
                            />
                        </div>

                        {error && (
                            <div className="text-red-400 text-sm bg-red-500/10 p-3 rounded-lg">
                                {error}
                            </div>
                        )}

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? 'Submitting...' : 'Submit Report'}
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}
