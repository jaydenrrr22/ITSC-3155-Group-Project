from . import orders, order_details, customers, ratings_reviews, payment_information, menu_items, promotions, resources, revenues, recipes



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(ratings_reviews.router)
    app.include_router(payment_information.router)
    app.include_router(menu_items.router)
    app.include_router(promotions.router)
    app.include_router(resources.router)
    app.include_router(recipes.router)
    app.include_router(revenues.router)