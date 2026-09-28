import { useEffect, useState } from "react";
import { Activity, ArrowUpRight, Check, LoaderCircle, RefreshCw, X } from "lucide-react";
import { Button } from "@/components/ui/button";

const apiBaseUrl = (import.meta.env.VITE_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

function App() {
  const [health, setHealth] = useState({ state: "checking", checkedAt: null });

  async function checkHealth() {
    setHealth((current) => ({ ...current, state: "checking" }));

    try {
      const response = await fetch(`${apiBaseUrl}/health`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const result = await response.json();
      if (result.status !== "ok") throw new Error("Unexpected health response");
      setHealth({ state: "healthy", checkedAt: new Date() });
    } catch {
      setHealth({ state: "unavailable", checkedAt: new Date() });
    }
  }

  useEffect(() => {
    checkHealth();
  }, []);

  const status = {
    checking: { label: "Checking", tone: "checking", Icon: LoaderCircle },
    healthy: { label: "Operational", tone: "healthy", Icon: Check },
    unavailable: { label: "Unavailable", tone: "unavailable", Icon: X },
  }[health.state];

  return (
    <main className="page-shell">
      <header className="topbar">
        <a className="brand" href="#home" aria-label="ESSL Reports home">
          <span className="brand-mark"><Activity size={17} strokeWidth={2.2} /></span>
          <span>ESSL <span className="brand-light">REPORTS</span></span>
        </a>
        <span className="environment"><span className="environment-dot" />LOCAL ENVIRONMENT</span>
      </header>

      <section className="content" aria-labelledby="page-title">
        <div className="eyebrow"><span>DEVELOPER CONSOLE</span><span className="eyebrow-rule" /></div>
        <div className="page-heading">
          <div>
            <p className="section-label">OVERVIEW / API</p>
            <h1 id="page-title">Service health</h1>
            <p className="description">A live connection check for the ESSL Reports API.</p>
          </div>
          <Button variant="outline" onClick={checkHealth} disabled={health.state === "checking"}>
            <RefreshCw size={15} className={health.state === "checking" ? "spin" : ""} />
            Refresh check
          </Button>
        </div>

        <section className={`status-panel status-${status.tone}`} aria-live="polite">
          <div className="status-main">
            <div className="status-icon"><status.Icon size={20} strokeWidth={2} /></div>
            <div>
              <p className="panel-label">API STATUS</p>
              <h2>{status.label}</h2>
            </div>
          </div>
          <div className="status-divider" />
          <div className="status-detail">
            <span className="detail-label">LAST CHECKED</span>
            <span className="detail-value">
              {health.checkedAt ? health.checkedAt.toLocaleTimeString() : "Waiting for response"}
            </span>
          </div>
          <div className="status-detail endpoint-detail">
            <span className="detail-label">ENDPOINT</span>
            <a className="detail-value endpoint-link" href={`${apiBaseUrl}/docs`} target="_blank" rel="noreferrer">
              {apiBaseUrl}/health <ArrowUpRight size={13} />
            </a>
          </div>
        </section>

        <footer className="page-footer">
          <span><span className="footer-dot" />Health endpoint responds with <code>status: ok</code></span>
          <span>ESSL REPORTS <span className="footer-version">/ 0.1.0</span></span>
        </footer>
      </section>
    </main>
  );
}

export default App;