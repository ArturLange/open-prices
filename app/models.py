from openfoodfacts import Flavor
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    mapped_column,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import force_auto_coercion
from sqlalchemy_utils.types.choice import ChoiceType

from app.db import Base
from app.enums import CurrencyEnum, LocationOSMEnum, PricePerEnum, ProofTypeEnum

force_auto_coercion()
JSONVariant = JSON().with_variant(JSONB(), "postgresql")


class User(Base):
    user_id: str = mapped_column(String, primary_key=True, index=True)
    price_count: int = mapped_column(
        Integer, nullable=False, server_default="0", index=True
    )
    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_moderator: bool = mapped_column(Boolean, nullable=False, server_default="false")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user")

    __tablename__ = "users"


class Session(Base):
    id: int = mapped_column(Integer, primary_key=True, index=True)

    user_id = mapped_column(
        String, ForeignKey("users.user_id"), index=True, nullable=False
    )
    user: Mapped[User] = relationship("User")

    token = mapped_column(String, unique=True, index=True, nullable=False)
    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_used = mapped_column(DateTime(timezone=True), nullable=True)

    __tablename__ = "sessions"


class Product(Base):
    id: int = mapped_column(Integer, primary_key=True, index=True)

    code: str = mapped_column(String, unique=True, index=True)

    source: Flavor = mapped_column(ChoiceType(Flavor))
    product_name: str = mapped_column(String)
    product_quantity: int = mapped_column(Integer)
    product_quantity_unit: str = mapped_column(String)
    categories_tags = mapped_column(ARRAY(String), server_default="{}", index=True)
    brands: str = mapped_column(String)
    brands_tags = mapped_column(ARRAY(String), server_default="{}", index=True)
    labels_tags = mapped_column(ARRAY(String), server_default="{}", index=True)
    image_url: str = mapped_column(String)
    unique_scans_n = mapped_column(Integer, nullable=False, server_default="0")

    prices: Mapped[list["Price"]] = relationship(back_populates="product")
    price_count: int = mapped_column(
        Integer, nullable=False, server_default="0", index=True
    )

    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __tablename__ = "products"


class Location(Base):
    id: int = mapped_column(Integer, primary_key=True, index=True)

    osm_id: int = mapped_column(BigInteger)
    osm_type: LocationOSMEnum = mapped_column(ChoiceType(LocationOSMEnum))
    osm_name = mapped_column(String)
    osm_display_name = mapped_column(String)
    osm_address_postcode = mapped_column(String)
    osm_address_city = mapped_column(String)
    osm_address_country = mapped_column(String)
    osm_lat = mapped_column(Numeric(precision=11, scale=7))
    osm_lon = mapped_column(Numeric(precision=11, scale=7))

    prices: Mapped[list["Price"]] = relationship(back_populates="location")
    price_count: int = mapped_column(
        Integer, nullable=False, server_default="0", index=True
    )

    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __tablename__ = "locations"


class Proof(Base):
    id = mapped_column(Integer, primary_key=True, index=True)

    file_path: str = mapped_column(String, nullable=False)
    mimetype = mapped_column(String, index=True)

    type: ProofTypeEnum = mapped_column(ChoiceType(ProofTypeEnum))
    is_public = mapped_column(
        Boolean, nullable=False, server_default="true", index=True
    )

    prices: Mapped[list["Price"]] = relationship(back_populates="proof")
    price_count: int = mapped_column(
        Integer, nullable=False, server_default="0", index=True
    )

    owner = mapped_column(String, index=True)

    created = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    __tablename__ = "proofs"


class Price(Base):
    id = mapped_column(Integer, primary_key=True, index=True)

    product_code = mapped_column(String, nullable=True, index=True)
    product_name = mapped_column(String, nullable=True)
    category_tag = mapped_column(String, nullable=True, index=True)
    labels_tags = mapped_column(JSONVariant, nullable=True, index=True)
    origins_tags = mapped_column(JSONVariant, nullable=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=True)
    product: Mapped[Product] = relationship(back_populates="prices")

    price = mapped_column(Numeric(precision=10, scale=2))
    price_is_discounted = mapped_column(Boolean, nullable=False, server_default="false")
    price_without_discount = mapped_column(
        Numeric(precision=10, scale=2), nullable=True
    )
    currency: CurrencyEnum = mapped_column(ChoiceType(CurrencyEnum))
    price_per: PricePerEnum = mapped_column(ChoiceType(PricePerEnum))

    location_osm_id = mapped_column(BigInteger, index=True)
    location_osm_type: LocationOSMEnum = mapped_column(ChoiceType(LocationOSMEnum))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=True)
    location: Mapped[Location] = relationship(back_populates="prices")

    date = mapped_column(Date)

    proof_id: Mapped[int] = mapped_column(ForeignKey("proofs.id"), nullable=True)
    proof: Mapped[Proof] = relationship(back_populates="prices")

    owner: str = mapped_column(String)

    created = mapped_column(DateTime(timezone=True), server_default=func.now())

    __tablename__ = "prices"
