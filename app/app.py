from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    migrate = Migrate(app, db)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route('/')
def home():
    return ''

# POST route for /restaurant_pizzas


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()

        # Extract data from the request
        restaurant_id = data.get('restaurant_id')
        pizza_id = data.get('pizza_id')
        price = data.get('price')

        # Validate data
        if not all([restaurant_id, pizza_id, price]):
            return jsonify({'error': 'Missing data'}), 400

        # Check if the restaurant and pizza exist
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if not restaurant or not pizza:
            return jsonify({'error': 'Restaurant or Pizza not found'}), 404

        # Create a new RestaurantPizza instance
        new_restaurant_pizza = RestaurantPizza(
            restaurant_id=restaurant_id,
            pizza_id=pizza_id,
            price=price
        )

        # Add to the database
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify({'message': 'RestaurantPizza created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE route for /restaurants/:id


@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    try:
        # Check if the restaurant exists
        restaurant = Restaurant.query.get(restaurant_id)

        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()

        return jsonify({'message': f'Restaurant with ID {restaurant_id} deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555)
