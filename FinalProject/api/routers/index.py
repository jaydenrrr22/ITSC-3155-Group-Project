from . import orders, order_details, customers, ratings_reviews, payment_information



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(ratings_reviews.router)
