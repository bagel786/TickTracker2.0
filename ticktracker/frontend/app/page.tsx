import SearchBar from './components/SearchBar';
import { TrendingUp, ShieldCheck, Zap } from 'lucide-react';

export default function Home() {
    return (
        <div className="flex-1 flex flex-col">
            {/* Hero Section */}
            <section className="relative flex flex-col items-center justify-center min-h-[80vh] px-4 text-center overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
                <div className="absolute inset-0 bg-gradient-to-b from-transparent via-dark/80 to-dark" />

                <div className="relative z-10 max-w-4xl mx-auto space-y-8">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm mb-4">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-sm text-gray-300">AI-Powered Price Predictions</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
                        Never Overpay for <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                            Live Events
                        </span> Again
                    </h1>

                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        TickTracker aggregates prices from major platforms and uses machine learning to predict the perfect time to buy.
                    </p>

                    <div className="pt-8">
                        <SearchBar />
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-24 px-4 bg-dark/50">
                <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
                    {[
                        {
                            icon: TrendingUp,
                            title: "Smart Predictions",
                            desc: "Our ML model analyzes historical data to forecast price trends with high accuracy."
                        },
                        {
                            icon: ShieldCheck,
                            title: "Verified Sources",
                            desc: "We only aggregate tickets from trusted platforms like Ticketmaster and Eventbrite."
                        },
                        {
                            icon: Zap,
                            title: "Real-time Alerts",
                            desc: "Get notified instantly when prices drop for your favorite events."
                        }
                    ].map((feature, i) => (
                        <div key={i} className="p-8 rounded-2xl bg-white/5 border border-white/10 hover:border-primary/50 transition-all">
                            <feature.icon className="w-10 h-10 text-primary mb-4" />
                            <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                            <p className="text-gray-400">{feature.desc}</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}
