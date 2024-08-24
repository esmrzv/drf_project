import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(name):
    try:
        product = stripe.Product.create(name=name)
        return product
    except Exception as e:
        print(f'Ошибка создания продукта {e}')
        return None


def create_price(price, product_id):
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id,
    )


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
