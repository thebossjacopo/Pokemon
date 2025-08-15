import React, { useEffect, useState } from "react";

type Deal = {
  deal_id: number;
  card_id: number;
  marketplace: string;
  url: string;
  price_eur: number;
  baseline_eur: number;
  discount_pct: number;
  card_name: string;
  set_name: string;
  number: string;
};

export default function Home() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const api = process.env.NEXT_PUBLIC_API_URL || "";
    fetch(api + "/deals")
      .then(r => r.json())
      .then(setDeals)
      .catch(e => setError(String(e)));
  }, []);

  return (
    <main style={{fontFamily:"system-ui, Arial", padding:20, maxWidth:900, margin:"0 auto"}}>
      <h1>JTB – Occasioni Carte Pokémon</h1>
      <p>Feed delle occasioni sotto baseline. Aggiorna automaticamente quando i dati sono disponibili.</p>
      {error && <p style={{color:"crimson"}}>Errore: {error}</p>}
      <table style={{width:"100%", borderCollapse:"collapse"}}>
        <thead>
          <tr>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Carta</th>
            <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Prezzo</th>
            <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Baseline</th>
            <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Sconto</th>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Marketplace</th>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Link</th>
          </tr>
        </thead>
        <tbody>
          {deals.map(d => (
            <tr key={d.deal_id}>
              <td style={{padding:"6px 4px"}}>{d.card_name} ({d.number}) – {d.set_name}</td>
              <td style={{textAlign:"right"}}>{d.price_eur.toFixed(2)} €</td>
              <td style={{textAlign:"right"}}>{d.baseline_eur.toFixed(2)} €</td>
              <td style={{textAlign:"right"}}>{(d.discount_pct*100).toFixed(0)}%</td>
              <td>{d.marketplace}</td>
              <td><a href={d.url} target="_blank" rel="noreferrer">Apri</a></td>
            </tr>
          ))}
          {!deals.length && <tr><td colSpan={6} style={{padding:"12px"}}>Nessun deal ancora disponibile.</td></tr>}
        </tbody>
      </table>
    </main>
  );
}
