from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from jtb_shared.db import SessionLocal, engine, Base
from jtb_shared import models
from jtb_shared.settings import INIT_TOKEN

app = FastAPI(title="JTB API Gateway", version="0.1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DealOut(BaseModel):
    deal_id: int
    card_id: int
    marketplace: str
    url: str
    price_eur: float
    baseline_eur: float
    discount_pct: float
    card_name: str
    set_name: str
    number: str

    class Config:
        from_attributes = True

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/init-db")
def init_db(token: str = Query(...), db: Session = Depends(get_db)):
    if token != INIT_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    Base.metadata.create_all(bind=engine)
    return {"status": "initialized"}

@app.post("/seed-demo")
def seed_demo(token: str = Query(...), db: Session = Depends(get_db)):
    if token != INIT_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # minimal demo data
    s = models.Set(name="Base Set", release_date="1999-01-09")
    db.add(s); db.flush()
    c = models.Card(set_id=s.set_id, name="Charizard", number="4/102", variant=None,
                    image_url="https://images.pokemontcg.io/base1/4_hires.png")
    db.add(c); db.flush()
    b = models.Baseline(card_id=c.card_id, condition="NM", language="EN",
                        window_days=30, median_price_eur=300.0, mean_price_eur=320.0,
                        stdev=40.0, q1=280.0, q3=350.0, iqr=70.0)
    db.add(b); db.flush()
    d = models.Deal(card_id=c.card_id, marketplace="DEMO", url="https://example.com/listing/123",
                    price_eur=220.0, baseline_eur=300.0, discount_pct=(300.0-220.0)/300.0)
    db.add(d); db.commit()
    return {"status": "seeded"}

@app.get("/deals", response_model=List[DealOut])
def list_deals(limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(models.Deal, models.Card, models.Set) \        .join(models.Card, models.Deal.card_id == models.Card.card_id) \        .join(models.Set, models.Card.set_id == models.Set.set_id) \        .order_by(models.Deal.deal_id.desc()).limit(limit)
    out = []
    for d, card, st in q.all():
        out.append(DealOut(
            deal_id=d.deal_id, card_id=d.card_id, marketplace=d.marketplace, url=d.url,
            price_eur=d.price_eur, baseline_eur=d.baseline_eur, discount_pct=d.discount_pct,
            card_name=card.name, set_name=st.name, number=card.number
        ))
    return out
