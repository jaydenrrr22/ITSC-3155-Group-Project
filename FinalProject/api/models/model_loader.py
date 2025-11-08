from . import orders, order_details, recipes, sandwiches, resources, Customers, Ratings_Reviews, menu_items

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    Customers.Base.metadata.create_all(engine)
    Ratings_Reviews.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)