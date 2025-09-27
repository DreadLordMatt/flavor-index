from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    season: Mapped[str | None] = mapped_column(String(255), nullable=True)
    taste: Mapped[str | None] = mapped_column(String(255), nullable=True)
    function: Mapped[str | None] = mapped_column(String(255), nullable=True)
    weight: Mapped[str | None] = mapped_column(String(255), nullable=True)
    volume: Mapped[str | None] = mapped_column(String(255), nullable=True)
    technique: Mapped[str | None] = mapped_column(Text, nullable=True)
    tips: Mapped[str | None] = mapped_column(Text, nullable=True)

    botanical_relatives: Mapped[List[BotanicalRelative]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
        default_factory=list,
    )
    related_ingredients: Mapped[List[RelatedIngredient]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
        default_factory=list,
    )
    flavor_affinities: Mapped[List[FlavorAffinity]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
        default_factory=list,
    )


class BotanicalRelative(Base):
    __tablename__ = "botanical_relatives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    ingredient: Mapped[Ingredient] = relationship(back_populates="botanical_relatives")


class RelatedIngredient(Base):
    __tablename__ = "related_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    ingredient: Mapped[Ingredient] = relationship(back_populates="related_ingredients")


class FlavorAffinity(Base):
    __tablename__ = "flavor_affinities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    ingredient: Mapped[Ingredient] = relationship(back_populates="flavor_affinities")
