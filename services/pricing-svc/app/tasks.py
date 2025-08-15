import os, time
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from jtb_shared.db import SessionLocal, engine
from jtb_shared import models

DISCOUNT_MIN = float(os.getenv("DEAL_MIN_DISCOUNT", "0.2"))
WINDOW_DAYS = int(os.getenv("WINDOW_DAYS", "30"))

def recompute_baselines():
    with SessionLocal() as db:
        # For each card with listings in last WINDOW_DAYS, compute robust stats
        cutoff = datetime.utcnow() - timedelta(days=WINDOW_DAYS)
        # gather card_ids
        card_ids = [cid for (cid,) in db.execute(select(models.Listing.card_id).where(models.Listing.listed_at >= cutoff).distinct())]
        for (card_id,) in card_ids:
            prices = [row[0] for row in db.execute(
                select(models.Listing.total_eur).where(
                    models.Listing.card_id==card_id, models.Listing.listed_at>=cutoff, models.Listing.status=="ACTIVE"
                )
            )]
            if not prices:
                continue
            arr = np.array(prices, dtype=float)
            q1, q3 = np.percentile(arr, [25, 75])
            iqr = float(q3 - q1)
            median = float(np.median(arr))
            mean = float(np.mean(arr))
            stdev = float(np.std(arr)) if len(arr) > 1 else 0.0
            # Upsert simplistic: delete existing baseline(s) for now and insert one
            db.query(models.Baseline).filter(models.Baseline.card_id==card_id).delete()
            db.add(models.Baseline(card_id=card_id, condition=None, language=None,
                                   window_days=WINDOW_DAYS, median_price_eur=median,
                                   mean_price_eur=mean, stdev=stdev, q1=float(q1), q3=float(q3), iqr=iqr,
                                   updated_at=datetime.utcnow()))
        db.commit()

def detect_deals():
    with SessionLocal() as db:
        # naive: compare each active listing to baseline (if exists)
        rows = db.execute(select(models.Listing, models.Baseline).join(
            models.Baseline, models.Baseline.card_id == models.Listing.card_id, isouter=True
        ).where(models.Listing.status=="ACTIVE")).all()
        for listing, baseline in rows:
            if not baseline or not baseline.median_price_eur:
                continue
            base = baseline.median_price_eur
            disc = (base - listing.total_eur) / base if base else 0.0
            if disc >= DISCOUNT_MIN:
                # avoid duplicates for same URL
                exists = db.execute(select(func.count()).select_from(models.Deal).where(models.Deal.url==listing.url)).scalar()
                if not exists:
                    db.add(models.Deal(card_id=listing.card_id, marketplace=listing.marketplace, url=listing.url,
                                       price_eur=listing.total_eur, baseline_eur=base, discount_pct=disc))
        db.commit()

def loop():
    # background loop for Render worker
    while True:
        try:
            recompute_baselines()
            detect_deals()
            print(f"[pricing] {datetime.utcnow().isoformat()} recomputed baselines and detected deals")
        except Exception as e:
            print("[pricing] error:", e)
        time.sleep(600)  # every 10 minutes

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["recompute", "detect", "loop"])
    args = p.parse_args()
    if args.cmd == "recompute":
        recompute_baselines()
        print("done")
    elif args.cmd == "detect":
        detect_deals()
        print("done")
    else:
        loop()

if __name__ == "__main__":
    main()
