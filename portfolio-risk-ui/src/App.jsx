import { Link, Route, Routes } from "react-router-dom";
import PricesPage from "./pages/PricesPage";
import HomePage from "./pages/HomePage";

export default function App() {
  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <nav style={{ marginBottom: "2rem" }}>
        <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
        <Link to="/prices">Prices</Link>
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/prices" element={<PricesPage />} />
      </Routes>
    </div>
  );
}