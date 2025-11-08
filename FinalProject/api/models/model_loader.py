from . import orders, order_details, recipes, sandwiches, resources, customers, ratings_reviews, payment_information, menu_items

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    ratings_reviews.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
