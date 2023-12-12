from app import create_app, db
from models import Restaurant, Pizza, RestaurantPizza

app = create_app()
app.app_context().push()

#sample data
restaurant1 = Restaurant()
restaurant2 = Restaurant()

Pepperoni = Pizza()
Margherita = Pizza()

restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1)
restaurant_pizza2 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2)

db.session.add_all([restaurant1, restaurant2, Pepperoni,
                   Margherita, restaurant_pizza1, restaurant_pizza2])

db.session.commit()


