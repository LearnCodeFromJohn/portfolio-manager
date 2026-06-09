export default function CompanyOverviewCard({ overview }) {
  if (!overview) return null;

  const formatPercent = (value) => {
    const num = Number(value);
    if (!num) return "N/A";
    return `${(num * 100).toFixed(2)}%`;
  };

  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "12px",
      padding: "1.5rem",
      marginTop: "1.5rem",
      marginBottom: "1.5rem",
      maxWidth: "900px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    }}>
      <h2>{overview.name} ({overview.symbol})</h2>
      <p><strong>Sector:</strong> {overview.sector}</p>
      <p><strong>Industry:</strong> {overview.industry}</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem" }}>
        <div><strong>Market Cap</strong><br />{(overview.market_cap)}</div>
        <div><strong>P/E Ratio</strong><br />{overview.pe_ratio}</div>
        <div><strong>Dividend Yield</strong><br />{formatPercent(overview.dividend_yield)}</div>
        <div><strong>Beta</strong><br />{overview.beta}</div>
      </div>

      <p style={{ marginTop: "1rem" }}>{overview.description}</p>
    </div>
  );
}