from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .db import Base

class Set(Base):
    __tablename__ = "sets"
    set_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    release_date: Mapped[str | None] = mapped_column(String(20))

class Card(Base):
    __tablename__ = "cards"
    card_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("sets.set_id"), index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    variant: Mapped[str | None] = mapped_column(String(50))
    image_url: Mapped[str | None] = mapped_column(Text)

    set: Mapped[Set] = relationship()

class Listing(Base):
    __tablename__ = "listings"
    listing_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.card_id"), index=True)
    marketplace: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(Text)
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    price: Mapped[float] = mapped_column(Float)         # item price only
    shipping: Mapped[float] = mapped_column(Float, default=0.0)  # shipping cost
    total_eur: Mapped[float] = mapped_column(Float)     # normalized price incl. shipping in EUR
    condition: Mapped[str | None] = mapped_column(String(20))
    language: Mapped[str | None] = mapped_column(String(10))
    listed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")

class Baseline(Base):
    __tablename__ = "baselines"
    baseline_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.card_id"), index=True)
    condition: Mapped[str | None] = mapped_column(String(20))
    language: Mapped[str | None] = mapped_column(String(10))
    window_days: Mapped[int] = mapped_column(Integer, default=30)
    median_price_eur: Mapped[float | None] = mapped_column(Float)
    mean_price_eur: Mapped[float | None] = mapped_column(Float)
    stdev: Mapped[float | None] = mapped_column(Float)
    q1: Mapped[float | None] = mapped_column(Float)
    q3: Mapped[float | None] = mapped_column(Float)
    iqr: Mapped[float | None] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Deal(Base):
    __tablename__ = "deals"
    deal_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.card_id"), index=True)
    marketplace: Mapped[str] = mapped_column(String(40))
    url: Mapped[str] = mapped_column(Text)
    price_eur: Mapped[float] = mapped_column(Float)
    baseline_eur: Mapped[float] = mapped_column(Float)
    discount_pct: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
