from . import (
    customers,
    orders,
    order_details,
    recipes,
    resources,
    ratings_reviews,
    payment_information,
    menu_items,
    promotions  # keep last if there are dependencies
)

from ..dependencies.database import Base, engine

def index():
    Base.metadata.create_all(engine)
