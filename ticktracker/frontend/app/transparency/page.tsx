'use client';

import {
    Database,
    EyeOff,
    BrainCircuit,
    TrendingUp,
    ShieldCheck,
    AlertTriangle,
    ArrowRight
} from 'lucide-react';
import Link from 'next/link';

export default function TransparencyPage() {
    return (
        <div className="min-h-screen p-8 bg-black">
            <div className="max-w-4xl mx-auto space-y-12">

                {/* Header */}
                <div className="text-center space-y-4 pt-8">
                    <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white mb-4 transition-colors">
                        ← Back to Search
                    </Link>
                    <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-500">
                        Model Transparency
                    </h1>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        How TickTracker reasons about prices, what verified data we use, and the limitations of our estimation model.
                    </p>
                </div>

                {/* Section 1: Data Sources */}
                <section className="bg-white/5 border border-white/10 rounded-2xl p-8 backdrop-blur-sm">
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400">
                            <Database className="w-8 h-8" />
                        </div>
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold text-white">Data Sources</h2>
                            <p className="text-gray-300">
                                TickTracker does not access private resale marketplaces or real-time secondary listings. Instead, we rely on a combination of verified primary sources and historical patterns.
                            </p>
                            <ul className="grid md:grid-cols-2 gap-3">
                                <li className="flex items-center gap-2 text-gray-400">
                                    <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                                    Ticketmaster & Eventbrite metadata
                                </li>
                                <li className="flex items-center gap-2 text-gray-400">
                                    <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                                    Historical pricing ranges
                                </li>
                                <li className="flex items-center gap-2 text-gray-400">
                                    <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                                    Event attributes (Venue, Artist)
                                </li>
                                <li className="flex items-center gap-2 text-gray-400">
                                    <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                                    Time-to-event progression
                                </li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* Section 2: What We Don't See */}
                <section className="bg-white/5 border border-white/10 rounded-2xl p-8 backdrop-blur-sm">
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-red-500/10 rounded-xl text-red-400">
                            <EyeOff className="w-8 h-8" />
                        </div>
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold text-white">What This Model Cannot See</h2>
                            <p className="text-gray-300">
                                To remain transparent, it’s important to understand what this model does <span className="text-white font-semibold">not</span> have access to:
                            </p>
                            <ul className="space-y-2">
                                <li className="flex items-center gap-2 text-gray-400">
                                    <AlertTriangle className="w-4 h-4 text-red-400" />
                                    Live resale prices from closed marketplaces (StubHub, VividSeats)
                                </li>
                                <li className="flex items-center gap-2 text-gray-400">
                                    <AlertTriangle className="w-4 h-4 text-red-400" />
                                    Individual seller behavior or desperation
                                </li>
                                <li className="flex items-center gap-2 text-gray-400">
                                    <AlertTriangle className="w-4 h-4 text-red-400" />
                                    Hidden fees or last-minute platform adjustments
                                </li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* Section 3: How We Reason */}
                <section className="bg-gradient-to-br from-primary/10 to-purple-900/10 border border-primary/20 rounded-2xl p-8">
                    <div className="flex items-start gap-4">
                        <div className="p-3 bg-primary/20 rounded-xl text-primary">
                            <BrainCircuit className="w-8 h-8" />
                        </div>
                        <div className="space-y-6 w-full">
                            <div>
                                <h2 className="text-2xl font-bold text-white">How Price Trends Are Estimated</h2>
                                <p className="text-gray-300 mt-2">
                                    Rather than predicting exact dollar amounts, TickTracker models price <strong>movement trends</strong> over time.
                                </p>
                            </div>

                            <div className="grid md:grid-cols-3 gap-4">
                                <div className="bg-black/20 p-4 rounded-xl border border-white/5">
                                    <h3 className="text-white font-semibold mb-2">1. Patterns</h3>
                                    <p className="text-sm text-gray-400">Events follow repeatable price–time standard deviations.</p>
                                </div>
                                <div className="bg-black/20 p-4 rounded-xl border border-white/5">
                                    <h3 className="text-white font-semibold mb-2">2. Urgency</h3>
                                    <p className="text-sm text-gray-400">Demand certainty increases as the event approaches.</p>
                                </div>
                                <div className="bg-black/20 p-4 rounded-xl border border-white/5">
                                    <h3 className="text-white font-semibold mb-2">3. Scarcity</h3>
                                    <p className="text-sm text-gray-400">Oversupply or verified sold-out status creates inflection points.</p>
                                </div>
                            </div>

                            <div className="bg-black/30 p-4 rounded-xl font-mono text-sm text-gray-300 border border-white/10 flex flex-col md:flex-row items-center justify-center gap-4 text-center">
                                <span>Estimated Price Trend</span>
                                <ArrowRight className="hidden md:block w-4 h-4 text-gray-500" />
                                <span className="text-primary font-bold">Time Pattern</span>
                                <span className="text-gray-500">×</span>
                                <span className="text-blue-400 font-bold">Demand Sensitivity</span>
                                <span className="text-gray-500">×</span>
                                <span className="text-green-400 font-bold">Scarcity Indicators</span>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Section 4: Confidence & Changes */}
                <div className="grid md:grid-cols-2 gap-6">
                    <section className="bg-white/5 border border-white/10 rounded-2xl p-8">
                        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            <TrendingUp className="w-5 h-5 text-yellow-400" />
                            Why Predictions Change
                        </h2>
                        <p className="text-gray-300 text-sm mb-4">
                            Predictions update as new signals emerge. This is expected behavior, not an error.
                        </p>
                        <ul className="space-y-2 text-sm text-gray-400">
                            <li>• Sudden verified ticket sell-outs</li>
                            <li>• Additional inventory releases by organizers</li>
                            <li>• Rapid drops in search volume demand</li>
                        </ul>
                    </section>

                    <section className="bg-white/5 border border-white/10 rounded-2xl p-8">
                        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            <ShieldCheck className="w-5 h-5 text-green-400" />
                            Confidence Score Meaning
                        </h2>
                        <p className="text-gray-300 text-sm mb-4">
                            Reflects how closely an event matches well-understood historical patterns.
                        </p>
                        <div className="space-y-3 text-sm">
                            <div>
                                <span className="text-green-400 font-bold block mb-1">High Confidence</span>
                                <span className="text-gray-400">Similar historical events, stable demand trends.</span>
                            </div>
                            <div>
                                <span className="text-yellow-400 font-bold block mb-1">Low Confidence</span>
                                <span className="text-gray-400">New/unique event, volatile changes, or limited data.</span>
                            </div>
                        </div>
                    </section>
                </div>

                {/* Footer Disclaimer */}
                <div className="border-t border-white/10 pt-8 text-center pb-12">
                    <p className="text-gray-500 text-sm max-w-2xl mx-auto">
                        <strong>Important Clarification:</strong> TickTracker is a decision-support tool, not a guarantee engine. We estimate trends based on available data, not investment advice. We are not affiliated with any ticket marketplace.
                    </p>
                </div>
            </div>
        </div>
    );
}
