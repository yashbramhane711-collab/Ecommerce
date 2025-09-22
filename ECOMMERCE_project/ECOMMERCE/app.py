from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from models.product import Product
from flask_login import current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.product import product_bp
    from routes.cart import cart_bp
    from routes.order import order_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context processor for cart count
    @app.context_processor
    def inject_cart_count():
        cart_count = 0
        if current_user.is_authenticated:
            from models.cart import CartItem
            cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
        return dict(cart_count=cart_count)
    
    # Create tables and sample data
    with app.app_context():
        db.create_all()
        try:
            from utils.seed import seed_data
            seed_data()
        except Exception as e:
            print(f"Error seeding data: {e}")
    
    # Basic routes
    @app.route('/')
    def index():
        products = Product.query.limit(6).all()
        return render_template('index.html', products=products)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)