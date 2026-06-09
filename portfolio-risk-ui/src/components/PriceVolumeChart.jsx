import { useMemo, useState } from "react";
import Highcharts from "highcharts";
import { HighchartsReact } from "highcharts-react-official";

const RANGE_OPTIONS = [
    { label: "5D", tradingDays: 5 },
    { label: "1M", months: 1 },
    { label: "3M", months: 3 },
];

export default function PriceVolumeChart({ prices, ticker }) {
    const [selectedRange, setSelectedRange] = useState("5D");

    const filteredPrices = useMemo(() => {
        if (!prices || prices.length === 0) return [];

        const sorted = [...prices].sort(
            (a, b) => new Date(a.date) - new Date(b.date)
        );

        const range = RANGE_OPTIONS.find((r) => r.label === selectedRange);

        // if (!range || range.months === null) {
        //     return sorted;
        // }

        if (range.tradingDays) {
            return sorted.slice(-range.tradingDays);
        }

        // Month-based fallback
        const latestDate = new Date(sorted[sorted.length - 1].date);
        const cutoffDate = new Date(latestDate);
        cutoffDate.setMonth(cutoffDate.getMonth() - range.months);

        return sorted.filter((p) => new Date(p.date) >= cutoffDate);
    }, [prices, selectedRange]);

    if (!prices || prices.length === 0) return null;

    const closePrices = filteredPrices.map((p) => [
        new Date(p.date).getTime(),
        Number(p.price),
    ]);
    const volumes = filteredPrices.map((p) => [
        new Date(p.date).getTime(),
        Number(p.volume),
    ]);

    const priceOptions = {
        title: { text: `${ticker}` },
        xAxis: { type: "datetime" },
        yAxis: { title: { text: "Price" } },
        tooltip: { shared: true },
        series: [
            {
                name: "Close Price",
                type: "line",
                data: closePrices,
            },
        ],
    };

    return (
        <div style={{ marginTop: "2rem" }}>
            <div style={{ marginBottom: "1rem" }}>
                {RANGE_OPTIONS.map((range) => (
                    <button
                        key={range.label}
                        onClick={() => setSelectedRange(range.label)}
                        style={{
                            marginRight: "0.5rem",
                            padding: "0.5rem 0.75rem",
                            borderRadius: "8px",
                            border:
                                selectedRange === range.label
                                    ? "2px solid black"
                                    : "1px solid grey",
                            background: selectedRange === range.label ? "#eee" : "#fff",
                            cursor: "pointer",
                        }}
                    >
                        {range.label}
                    </button>
                ))}
            </div>

            <div style={{ marginBottom: "2rem" }}>
                <HighchartsReact highcharts={Highcharts} options={priceOptions} />
            </div>
        </div>
    );
}