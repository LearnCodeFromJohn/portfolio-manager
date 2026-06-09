import { useState, useEffect } from "react";
import PriceVolumeChart from "../components/PriceVolumeChart";
import CompanyOverviewCard from "../components/CompanyOverviewCard";
import { getWatchlist, addToWatchlist, removeFromWatchlist } from "../utils/watchlist";

const API_URL = "https://n7nbh098ra.execute-api.us-east-1.amazonaws.com";

export default function PricesPage() {
    const [ticker, setTicker] = useState("AAPL");
    const [prices, setPrices] = useState([]);
    const [message, setMessage] = useState("");
    const [overview, setOverview] = useState(null);
    const [watchlist, setWatchlist] = useState([]);

    useEffect(() => {
        setWatchlist(getWatchlist());
    }, []);

    async function getPrices() {
        setMessage("Loading prices and company info...");

        const [pricesRes, overviewRes] = await Promise.all([
            fetch(`${API_URL}/prices?ticker=${ticker}`),
            fetch(`${API_URL}/company/overview?ticker=${ticker}`),
        ]);

        const pricesData = await pricesRes.json();
        const overviewData = await overviewRes.json();

        setPrices(pricesData.prices || []);
        setOverview(overviewData);
        setMessage(`Loading prices for ${ticker}`);

        const updated = addToWatchlist(ticker);
        setWatchlist(updated);
    }

    return (
        <>
            <h1>Stock Prices</h1>

            <input
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Ticker"
            />
            <button onClick={getPrices}>Get Prices</button>

            <p>{message}</p>
            <CompanyOverviewCard overview={overview} />
            <div style={{ marginTop: "1rem" }}>
                <h3>Watchlist</h3>

                {watchlist.length === 0 && <p>No tickers yet</p>}

                {watchlist.map((t) => (
                    <button
                        key={t}
                        onClick={() => setTicker(t)}
                        style={{
                            marginRight: "0.5rem",
                            marginBottom: "0.5rem",
                            padding: "0.4rem 0.7rem",
                            borderRadius: "8px",
                            border: "1px solid #ccc",
                            cursor: "pointer",
                        }}
                    >
                        {t}
                    </button>
                ))}
            </div>
            <PriceVolumeChart prices={prices} ticker={ticker} />
        </>
    );
}